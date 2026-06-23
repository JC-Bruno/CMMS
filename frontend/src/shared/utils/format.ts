export function humanizeValue(value?: string | number | null) {
  if (value === undefined || value === null || value === "") {
    return "Sin dato";
  }

  return String(value)
    .replaceAll("_", " ")
    .replaceAll("-", " ")
    .replace(/\b\w/g, (letter) => letter.toUpperCase());
}

export function formatQuantity(value?: string | number | null) {
  if (value === undefined || value === null || value === "") {
    return "0.00";
  }

  const numberValue = Number(value);

  if (Number.isNaN(numberValue)) {
    return String(value);
  }

  return numberValue.toFixed(2);
}