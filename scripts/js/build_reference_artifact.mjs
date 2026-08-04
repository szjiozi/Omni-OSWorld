#!/usr/bin/env node

import fs from "node:fs/promises";
import path from "node:path";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";
import JSZip from "jszip";

const [blueprintPath, outputPath, previewDir, qaPath] = process.argv.slice(2);
if (!blueprintPath || !outputPath || !previewDir || !qaPath) {
  throw new Error(
    "Usage: build_reference_artifact.mjs BLUEPRINT OUTPUT_XLSX PREVIEW_DIR QA_JSON",
  );
}

const blueprint = JSON.parse(await fs.readFile(blueprintPath, "utf8"));
const workbook = Workbook.create();

function columnName(index) {
  let value = index + 1;
  let name = "";
  while (value > 0) {
    value -= 1;
    name = String.fromCharCode(65 + (value % 26)) + name;
    value = Math.floor(value / 26);
  }
  return name;
}

function convertValue(value, type) {
  if (value === "") return null;
  if (type === "integer") {
    const parsed = Number.parseInt(value, 10);
    if (!Number.isFinite(parsed)) throw new Error(`Invalid integer: ${value}`);
    return parsed;
  }
  if (type === "decimal" || type === "currency") {
    const parsed = Number(value);
    if (!Number.isFinite(parsed)) throw new Error(`Invalid number: ${value}`);
    return parsed;
  }
  if (type === "date") {
    const parsed = new Date(`${value}T00:00:00Z`);
    if (Number.isNaN(parsed.getTime())) throw new Error(`Invalid date: ${value}`);
    return parsed;
  }
  return value;
}

const qaSheets = [];
const autoFilterTables = [];
await fs.mkdir(path.dirname(outputPath), { recursive: true });
await fs.mkdir(previewDir, { recursive: true });

for (const [sheetIndex, spec] of blueprint.sheets.entries()) {
  const sheet = workbook.worksheets.add(spec.name);
  sheet.showGridLines = false;
  const width = spec.headers.length;
  const lastColumn = columnName(width - 1);
  sheet.getRange(`A1:${lastColumn}1`).values = [spec.headers];
  sheet.getRange(`A1:${lastColumn}1`).format = {
    fill: "#1F4E78",
    font: { bold: true, color: "#FFFFFF" },
    rowHeight: 24,
    verticalAlignment: "center",
  };
  const values = spec.rows.map((row) =>
    row.values.map((value, index) => convertValue(value, spec.column_types[index])),
  );
  const lastDataRow = values.length + 1;
  sheet.getRange(`A2:${lastColumn}${lastDataRow}`).values = values;

  for (const formula of spec.formulas) {
    sheet.getRange(formula.cell).formulas = [[formula.formula]];
  }
  for (let index = 0; index < width; index += 1) {
    const column = columnName(index);
    const dataRange = sheet.getRange(`${column}2:${column}${lastDataRow}`);
    dataRange.format.numberFormat = spec.column_number_formats[index];
    const maxLength = Math.max(
      spec.headers[index].length,
      ...spec.rows.map((row) => String(row.values[index]).length),
    );
    sheet.getRange(`${column}:${column}`).format.columnWidth = Math.min(
      28,
      Math.max(12, maxLength + 4),
    );
  }
  sheet.getRange(`A1:${lastColumn}${lastDataRow}`).format.borders = {
    insideHorizontal: { style: "thin", color: "#D9E2F3" },
    bottom: { style: "thin", color: "#A6B7C8" },
  };
  if (spec.freeze_header_row) sheet.freezePanes.freezeRows(1);
  if (spec.autofilter_range !== null) {
    const table = sheet.tables.add(spec.autofilter_range, true);
    table.name = `ReferenceData${sheetIndex + 1}`;
    autoFilterTables.push({
      tableNumber: autoFilterTables.length + 1,
      range: spec.autofilter_range,
    });
  }

  const inspection = await workbook.inspect({
    kind: "table",
    sheetId: spec.name,
    range: `A1:${lastColumn}${Math.min(lastDataRow, 12)}`,
    include: "values,formulas",
    tableMaxRows: 12,
    tableMaxCols: 20,
    maxChars: 5000,
  });
  const preview = await workbook.render({
    sheetName: spec.name,
    autoCrop: "all",
    scale: 1.5,
    format: "png",
  });
  const previewPath = path.join(previewDir, `${spec.name.replace(/[^A-Za-z0-9_-]/g, "_")}.png`);
  await fs.writeFile(previewPath, new Uint8Array(await preview.arrayBuffer()));
  qaSheets.push({
    name: spec.name,
    preview_path: previewPath,
    inspection: inspection.ndjson,
  });
}

const formulaErrors = await workbook.inspect({
  kind: "match",
  searchTerm: "#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",
  options: { useRegex: true, maxResults: 300 },
  summary: "final formula error scan",
  maxChars: 5000,
});
const output = await SpreadsheetFile.exportXlsx(workbook);
let outputData = output.data;
if (autoFilterTables.length > 0) {
  const archive = await JSZip.loadAsync(outputData);
  for (const autoFilter of autoFilterTables) {
    const tablePath = `xl/tables/table${autoFilter.tableNumber}.xml`;
    const tableFile = archive.file(tablePath);
    if (tableFile === null) throw new Error(`Missing XLSX table part: ${tablePath}`);
    const tableXml = await tableFile.async("string");
    if (!tableXml.includes("<x:autoFilter")) {
      archive.file(
        tablePath,
        tableXml.replace(
          /(<x:table\b[^>]*>)/,
          `$1<x:autoFilter ref="${autoFilter.range}" />`,
        ),
      );
    }
  }
  outputData = await archive.generateAsync({ type: "uint8array" });
}
await fs.writeFile(outputPath, outputData);
await fs.writeFile(
  qaPath,
  `${JSON.stringify(
    {
      workbook_title: blueprint.workbook_title,
      output_path: outputPath,
      manual_setup_steps: blueprint.manual_setup_steps,
      sheets: qaSheets,
      formula_error_scan: formulaErrors.ndjson,
    },
    null,
    2,
  )}\n`,
  "utf8",
);
