import { create } from "zustand";
import { studentsApi } from "../api/students";
import type { Student } from "../../entities/student";
import { useLoaderStore } from "./loaderStore";

interface StudentStore {
  students: Student[];
  isLoaded: boolean;
  setStudent: (force?: boolean) => Promise<void>;
  createStudent: (student: Omit<Student, "id">) => Promise<void>;
  updateStudent: (
    student_id: string,
    student: Partial<Student>,
  ) => Promise<void>;
  getById: (student_id: string) => Promise<Student>;
}

export const useStudentStore = create<StudentStore>((set, get) => ({
  students: [],
  isLoaded: false,

  setStudent: async (force) => {
    if (get().isLoaded && !force) {
      return;
    }

    await useLoaderStore.getState().withLoader(async () => {
      const students = await studentsApi.getAll();

      set({
        students: students.data,
        isLoaded: true,
      });
    });
  },

  createStudent: async (student) => {
    await useLoaderStore.getState().withLoader(async () => {
      const { create } = studentsApi;

      await create(student);
      await get().setStudent(true);
    });
  },

  updateStudent: async (student_id, student) => {
    await useLoaderStore.getState().withLoader(async () => {
      const { update } = studentsApi;

      await update(student_id, student);
      await get().setStudent(true);
    });
  },

  getById: async (student_id) => {
    return useLoaderStore.getState().withLoader(async () => {
      const { getById } = studentsApi;

      const student = await getById(student_id);

      return student.data;
    });
  },
}));

export const useStudent = () => {
  const { students, setStudent, createStudent, updateStudent, getById } =
    useStudentStore();

  return {
    students,
    setStudent,
    createStudent,
    updateStudent,
    getById,
  };
};
