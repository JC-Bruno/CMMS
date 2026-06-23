type LoadingStateProps = {
  message?: string;
};

export function LoadingState({
  message = "Cargando información...",
}: LoadingStateProps) {
  return (
    <div className="feedback-state">
      <div className="feedback-state__spinner" />
      <p className="feedback-state__title">{message}</p>
    </div>
  );
}