type StatusBadgeVariant = "success" | "warning" | "danger" | "info" | "neutral";

type StatusBadgeProps = {
  label: string;
  variant?: StatusBadgeVariant;
};

export function StatusBadge({
  label,
  variant = "neutral",
}: StatusBadgeProps) {
  return <span className={`status-badge status-badge--${variant}`}>{label}</span>;
}