import { api } from "./client";
import type { Student } from "../../entities/student";

export const studentsApi = {
  getAll() {
    return api.get("/students/");
  },

  getById(student_id: string) {
    return api.get(`/students/${student_id}`);
  },

  create(student_cred: Omit<Student, "id">) {
    return api.post("/students", student_cred);
  },

  update(student_id: string, student_cred: Partial<Student>) {
    return api.patch(`/students/${student_id}`, student_cred);
  },

  delete(student_id: string) {
    return api.delete(`/students/${student_id}`);
  },
};
