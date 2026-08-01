import { create } from "zustand";

interface LoaderStore {
  loading: boolean;
  show: () => void;
  hide: () => void;
  withLoader: <T>(callback: () => Promise<T>) => Promise<T>;
}

export const useLoaderStore = create<LoaderStore>((set) => ({
  loading: false,

  show: () => set({ loading: true }),

  hide: () => set({ loading: false }),

  withLoader: async (callback) => {
    set({ loading: true });

    try {
      return await callback();
    } finally {
      set({ loading: false });
    }
  },
}));

export const useLoader = () => {
  const { loading, show, hide, withLoader } = useLoaderStore();

  return {
    loading,
    show,
    hide,
    withLoader,
  };
};
