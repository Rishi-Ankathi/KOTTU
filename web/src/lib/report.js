/**
 * Parse the sklearn classification report text into per-class rows.
 * Assumes numeric class labels (0 .. n-1), which is what KOTTU's
 * LabelEncoder produces.
 */
export function parseReport(text) {
  const rows = [];
  for (const line of text.split("\n")) {
    const parts = line.trim().split(/\s+/);
    if (parts.length === 5 && /^-?\d+$/.test(parts[0])) {
      rows.push({
        cls: Number(parts[0]),
        precision: Number(parts[1]),
        recall: Number(parts[2]),
        f1: Number(parts[3]),
        support: Number(parts[4]),
      });
    }
  }
  return rows;
}
