export type PaginatedApiResponse<T> = {
  count?: number;
  next?: string | null;
  previous?: string | null;
  results: T[];
};

export type ApiListResponse<T> = T[] | PaginatedApiResponse<T>;

export function getApiResponseItems<T>(data: ApiListResponse<T>): T[] {
  if (Array.isArray(data)) {
    return data;
  }

  return data.results;
}