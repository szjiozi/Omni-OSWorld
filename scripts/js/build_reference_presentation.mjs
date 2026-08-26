#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";

const require = createRequire(import.meta.url);
const pptxgen = require("pptxgenjs");
const sharp = require("sharp");

function fail(message) {
  throw new Error(message);
}

function imageSvg(kind, palette) {
  const { primary, secondary, accent, background } = palette;
  if (kind === "botanical") {
    return `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800">
      <path d="M600 720C580 540 580 360 605 115" fill="none" stroke="#${primary}" stroke-width="28" stroke-linecap="round"/>
      <ellipse cx="455" cy="480" rx="150" ry="72" transform="rotate(28 455 480)" fill="#${secondary}"/>
      <ellipse cx="735" cy="345" rx="150" ry="72" transform="rotate(-30 735 345)" fill="#${primary}"/>
      <circle cx="610" cy="150" r="72" fill="#${accent}"/>
      <circle cx="610" cy="150" r="30" fill="#${primary}"/>
    </svg>`;
  }
  if (kind === "pollinator") {
    return `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800">
      <path d="M210 720C260 505 360 360 505 250" fill="none" stroke="#${primary}" stroke-width="24"/>
      <circle cx="360" cy="520" r="90" fill="#${accent}"/>
      <circle cx="360" cy="520" r="34" fill="#${primary}"/>
      <ellipse cx="745" cy="335" rx="155" ry="92" fill="#${accent}" stroke="#${primary}" stroke-width="16"/>
      <rect x="665" y="260" width="28" height="150" fill="#${primary}"/>
      <rect x="735" y="245" width="28" height="180" fill="#${primary}"/>
      <rect x="805" y="265" width="28" height="140" fill="#${primary}"/>
      <ellipse cx="660" cy="210" rx="120" ry="75" transform="rotate(-25 660 210)" fill="#${secondary}" opacity="0.7"/>
      <ellipse cx="840" cy="210" rx="120" ry="75" transform="rotate(25 840 210)" fill="#${secondary}" opacity="0.7"/>
    </svg>`;
  }
  if (kind === "garden") {
    return `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800">
      <path d="M210 590L600 430l390 160-390 160z" fill="#${accent}" stroke="#${primary}" stroke-width="18"/>
      <path d="M270 575l330-120 330 120-330 130z" fill="#${secondary}"/>
      <path d="M440 540c-5-105 25-170 85-220" fill="none" stroke="#${primary}" stroke-width="18"/>
      <ellipse cx="470" cy="360" rx="90" ry="42" transform="rotate(30 470 360)" fill="#${primary}"/>
      <ellipse cx="570" cy="300" rx="90" ry="42" transform="rotate(-28 570 300)" fill="#${secondary}"/>
      <path d="M690 540c-5-105 25-170 85-220" fill="none" stroke="#${primary}" stroke-width="18"/>
      <ellipse cx="720" cy="360" rx="90" ry="42" transform="rotate(30 720 360)" fill="#${primary}"/>
      <ellipse cx="820" cy="300" rx="90" ry="42" transform="rotate(-28 820 300)" fill="#${secondary}"/>
    </svg>`;
  }
  if (kind === "map") {
    return `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800">
      <rect width="1200" height="800" fill="#${background}"/>
      <path d="M160 660l250-105 300 100 330-125V145L710 270 410 170 160 275z" fill="#${secondary}" opacity="0.65"/>
      <path d="M215 580C375 400 510 470 655 315s250-80 330-170" fill="none" stroke="#${primary}" stroke-width="34" stroke-linecap="round" stroke-dasharray="28 22"/>
      <circle cx="230" cy="565" r="42" fill="#${accent}"/>
      <circle cx="975" cy="155" r="42" fill="#${accent}"/>
    </svg>`;
  }
  if (kind === "person") {
    return `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800">
      <rect width="1200" height="800" fill="#${background}"/>
      <circle cx="600" cy="270" r="135" fill="#${accent}"/>
      <path d="M270 760c25-230 150-350 330-350s305 120 330 350" fill="#${primary}"/>
      <circle cx="560" cy="250" r="14" fill="#${secondary}"/>
      <circle cx="640" cy="250" r="14" fill="#${secondary}"/>
      <path d="M550 325c35 28 65 28 100 0" fill="none" stroke="#${secondary}" stroke-width="14" stroke-linecap="round"/>
    </svg>`;
  }
  if (kind === "product") {
    return `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800">
      <rect width="1200" height="800" fill="#${background}"/>
      <ellipse cx="600" cy="690" rx="350" ry="55" fill="#${secondary}" opacity="0.25"/>
      <rect x="350" y="170" width="500" height="470" rx="55" fill="#${primary}"/>
      <rect x="405" y="225" width="390" height="275" rx="22" fill="#${secondary}"/>
      <circle cx="600" cy="565" r="32" fill="#${accent}"/>
    </svg>`;
  }
  if (kind === "document") {
    return `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800">
      <rect width="1200" height="800" fill="#${background}"/>
      <rect x="300" y="90" width="600" height="620" rx="24" fill="#FFFFFF" stroke="#${primary}" stroke-width="18"/>
      <rect x="390" y="210" width="420" height="36" fill="#${accent}"/>
      <rect x="390" y="310" width="330" height="24" fill="#${secondary}"/>
      <rect x="390" y="385" width="420" height="24" fill="#${secondary}"/>
      <rect x="390" y="460" width="280" height="24" fill="#${secondary}"/>
    </svg>`;
  }
  return `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="800">
    <rect width="1200" height="800" fill="#${background}"/>
    <circle cx="955" cy="170" r="92" fill="#${accent}"/>
    <path d="M0 650L300 360l190 175 205-275 505 390v150H0z" fill="#${primary}"/>
    <path d="M0 735L420 475l210 170 205-140 365 230v65H0z" fill="#${secondary}"/>
  </svg>`;
}

async function imageData(kind, theme) {
  const svg = imageSvg(kind, {
    primary: theme.primary_color,
    secondary: theme.secondary_color,
    accent: theme.accent_color,
    background: theme.background_color,
  });
  const png = await sharp(Buffer.from(svg)).png().toBuffer();
  return `image/png;base64,${png.toString("base64")}`;
}

function shapeType(pptx, kind) {
  const mapping = {
    rect: pptx.ShapeType.rect,
    round_rect: pptx.ShapeType.roundRect,
    ellipse: pptx.ShapeType.ellipse,
    chevron: pptx.ShapeType.chevron,
    line: pptx.ShapeType.line,
  };
  return mapping[kind] || pptx.ShapeType.rect;
}

function textOptions(item) {
  const s = item.style;
  return {
    x: item.x,
    y: item.y,
    w: item.w,
    h: item.h,
    fontFace: s.font_face,
    fontSize: s.font_size,
    color: s.text_color,
    bold: s.bold,
    italic: s.italic,
    underline: s.underline,
    align: s.align,
    valign: s.valign === "mid" ? "mid" : s.valign,
    margin: 0.08,
    breakLine: false,
    fit: "shrink",
    fill: { color: s.fill_color, transparency: 100 },
    line: { color: s.line_color, transparency: 100 },
    altText: item.semantic_id,
  };
}

async function addObject(pptx, slide, item, theme) {
  const s = item.style;
  const common = { x: item.x, y: item.y, w: item.w, h: item.h };
  if (item.type === "text") {
    slide.addText(item.content.text, textOptions(item));
    return;
  }
  if (item.type === "shape") {
    slide.addShape(shapeType(pptx, item.content.shape_kind), {
      ...common,
      fill: { color: s.fill_color },
      line: { color: s.line_color, width: 1.25 },
      altText: item.semantic_id,
    });
    if (item.content.text) {
      slide.addText(item.content.text, {
        ...textOptions(item),
        fill: { color: s.fill_color, transparency: 100 },
        line: { color: s.line_color, transparency: 100 },
        altText: `${item.semantic_id}_label`,
      });
    }
    return;
  }
  if (item.type === "image") {
    slide.addImage({
      data: await imageData(item.content.image_kind, theme),
      ...common,
      altText: item.semantic_id,
    });
    return;
  }
  if (item.type === "table") {
    const rows = item.content.rows.map((row, rowIndex) =>
      row.map((value) => ({
        text: value,
        options: rowIndex === 0
          ? { bold: true, color: "FFFFFF", fill: { color: theme.primary_color } }
          : { color: s.text_color, fill: { color: s.fill_color } },
      })),
    );
    slide.addTable(rows, {
      ...common,
      border: { pt: 1, color: s.line_color },
      fontFace: s.font_face,
      fontSize: s.font_size,
      color: s.text_color,
      margin: 0.06,
      altText: item.semantic_id,
    });
    return;
  }
  if (item.type === "chart") {
    const chartData = item.content.series.map((entry) => ({
      name: entry.name,
      labels: item.content.categories,
      values: entry.values,
    }));
    slide.addChart(pptx.ChartType.bar, chartData, {
      ...common,
      barDir: "col",
      chartColors: [theme.primary_color, theme.accent_color, theme.secondary_color],
      showLegend: chartData.length > 1,
      legendPos: "b",
      showValue: true,
      dataLabelPosition: "outEnd",
      catAxisLabelColor: s.text_color,
      valAxisLabelColor: s.text_color,
      valGridLine: { color: "D9E0E7", size: 0.5 },
      catGridLine: { style: "none" },
      showTitle: false,
      altText: item.semantic_id,
    });
    return;
  }
  fail(`Unsupported object type: ${item.type}`);
}

function geometricWarnings(blueprint) {
  const warnings = [];
  for (const slide of blueprint.slides) {
    const objects = slide.objects;
    for (let i = 0; i < objects.length; i += 1) {
      for (let j = i + 1; j < objects.length; j += 1) {
        const a = objects[i];
        const b = objects[j];
        const overlapW = Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x);
        const overlapH = Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y);
        if (overlapW > 0.08 && overlapH > 0.08) {
          warnings.push({
            slide_number: slide.slide_number,
            objects: [a.semantic_id, b.semantic_id],
            overlap_area: Number((overlapW * overlapH).toFixed(4)),
          });
        }
      }
    }
  }
  return warnings;
}

async function main() {
  const [blueprintPath, outputPath, qaSeedPath] = process.argv.slice(2);
  if (!blueprintPath || !outputPath || !qaSeedPath) {
    fail("usage: build_reference_presentation.mjs BLUEPRINT OUTPUT_PPTX QA_SEED");
  }
  const blueprint = JSON.parse(fs.readFileSync(blueprintPath, "utf8"));
  const pptx = new pptxgen();
  pptx.layout = blueprint.slide_size === "wide" ? "LAYOUT_WIDE" : "LAYOUT_4X3";
  pptx.author = "OSWorld Expert Skill Reference Pipeline";
  pptx.subject = "Synthetic editable reference-task initial artifact";
  pptx.title = blueprint.presentation_title;
  pptx.company = "OSWorld";
  pptx.lang = "en-US";
  pptx.theme = {
    headFontFace: blueprint.theme.title_font,
    bodyFontFace: blueprint.theme.body_font,
    lang: "en-US",
  };

  for (const slideSpec of blueprint.slides) {
    const slide = pptx.addSlide();
    slide.background = { color: slideSpec.background_color };
    for (const item of slideSpec.objects) {
      await addObject(pptx, slide, item, blueprint.theme);
    }
  }

  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  await pptx.writeFile({ fileName: outputPath });
  fs.writeFileSync(qaSeedPath, JSON.stringify({
    schema_version: "1.0",
    slide_count: blueprint.slides.length,
    semantic_object_count: blueprint.slides.reduce((n, s) => n + s.objects.length, 0),
    geometric_overlap_warnings: geometricWarnings(blueprint),
  }, null, 2) + "\n");
}

main().catch((error) => {
  console.error(error.stack || error.message || String(error));
  process.exitCode = 1;
});
