import { useCallback, useEffect, useState } from "react";

type UseApiDataResult<T> = {
  data: T | null;
  error: string;
  isLoading: boolean;
  reload: () => Promise<void>;
};

export function useApiData<T>(loader: () => Promise<T>): UseApiDataResult<T> {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(true);

  const reload = useCallback(async () => {
    setIsLoading(true);
    setError("");

    try {
      const result = await loader();
      setData(result);
    } catch (error) {
      const message =
        error instanceof Error
          ? error.message
          : "No se pudo cargar la información.";

      setError(message);
      setData(null);
    } finally {
      setIsLoading(false);
    }
  }, [loader]);

  useEffect(() => {
    void reload();
  }, [reload]);

  return {
    data,
    error,
    isLoading,
    reload,
  };
}