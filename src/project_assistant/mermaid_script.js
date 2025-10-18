// /app/scripts/mermaid_script.js
import fs from "node:fs";
import path from "node:path";
import { run } from "@mermaid-js/mermaid-cli";

/**
 * Usage: node /app/scripts/mermaid_script.js <input.mmd> <output.svg>
 */
async function main() {
  const [inputPath, outputPath] = process.argv.slice(2);
  if (!inputPath || !outputPath) {
    console.error("Usage: node mermaid_script.js <input.mmd> <output.svg>");
    process.exit(1);
  }

  // Ensure output directory exists
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });

  await run(inputPath, outputPath, {
    outputFormat: "svg", // explicit format
    mermaidConfig: {
      securityLevel: "strict",
      flowchart: { useMaxWidth: true, htmlLabels: true },
    },
    puppeteerConfig: {
      args: [
        "--no-sandbox",
        "--disable-setuid-sandbox",
        "--disable-dev-shm-usage",
      ],
    },
  });

  console.log(`SVG written to ${outputPath}`);
}

main().catch((err) => {
  console.error("Failed to render SVG:", err);
  process.exit(1);
});
