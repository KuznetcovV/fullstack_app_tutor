import { create } from "zustand";

interface LoaderStore {
  loading: boolean;
  show: () => void;
  hide: () => void;
}

export const useLoaderStore = create<LoaderStore>((set) => ({
  loading: false,

  show: () => set({ loading: true }),

  hide: () => set({ loading: false }),
}));

export const useLoader = () => {
  const loading = useLoaderStore((state) => state.loading);

  const show = useLoaderStore((state) => state.show);

  const hide = useLoaderStore((state) => state.hide);

  return {
    loading,
    show,
    hide,
  };
};
