import { api } from "./client";
import type { Lesson } from "../../entities/lesson";

export const lessonsApi = {
  getAll() {
    return api.get("/lessons");
  },
  create(lesson_cred: Omit<Lesson, "id">) {
    return api.post("/lessons", lesson_cred);
  },
};
