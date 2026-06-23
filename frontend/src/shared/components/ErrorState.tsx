type ErrorStateProps = {
  title?: string;
  description: string;
  onRetry?: () => void;
};

export function ErrorState({
  title = "No se pudo cargar la información",
  description,
  onRetry,
}: ErrorStateProps) {
  return (
    <div className="feedback-state feedback-state--error">
      <div className="feedback-state__icon">!</div>
      <h3 className="feedback-state__title">{title}</h3>
      <p className="feedback-state__description">{description}</p>

      {onRetry ? (
        <button className="button button--secondary" onClick={onRetry}>
          Reintentar
        </button>
      ) : null}
    </div>
  );
}