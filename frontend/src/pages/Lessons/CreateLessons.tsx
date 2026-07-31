import { useState } from "react";
import Input from "../../shared/ui/input";
import Button from "../../shared/ui/button";
import { lessonsApi } from "../../shared/api/lessons";
import type { Lesson } from "../../entities/lesson";

export default function CreateLessons() {
  const { create } = lessonsApi;
  const [lesson, setLesson] = useState<Omit<Lesson, "id">>({
    student_id: 0,
    day: 1,
    time_start: "",
    time_end: "",
  });

  return (
    <div>
      <h1>Создание урока</h1>
      <Input
        label="Имя"
        value={lesson.student_id || ""}
        onChange={(value) =>
          setLesson({ ...lesson, student_id: Number(value) })
        }
      />
      <Input
        label="День"
        type="number"
        min={1}
        max={7}
        value={String(lesson.day || 1)}
        onChange={(value) => setLesson({ ...lesson, day: Number(value) })}
      />
      <Input
        label="Время начала"
        type="time"
        value={lesson.time_start || ""}
        onChange={(value) =>
          setLesson({ ...lesson, time_start: String(value) })
        }
      />
      <Input
        label="Время окончания"
        type="time"
        value={lesson.time_end || ""}
        onChange={(value) => setLesson({ ...lesson, time_end: String(value) })}
      />
      <Button
        label="Создать"
        onClick={() => {
          create(lesson);
        }}
      />
    </div>
  );
}
