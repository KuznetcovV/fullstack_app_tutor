import { useState } from "react";
import Input from "../../shared/ui/input";
import Button from "../../shared/ui/button";
import { useStudent } from "../../shared/store/studentStore";
import type { Student } from "../../entities/student";
import styles from "./CreateStudents.module.css";
// import { useNavigate } from "react-router-dom";

export default function CreateStudents() {
  const { createStudent } = useStudent();
  // const navigate = useNavigate();
  const [student, setStudent] = useState<Omit<Student, "id">>({
    first_name: "",
    last_name: "",
    number_of_class: 1,
  });

  return (
    <div className={styles.main}>
      <h1 className={styles.title}>Создание ученика</h1>

      <div className={styles.form}>
        <Input
          label="Имя"
          value={student.first_name || ""}
          onChange={(value) =>
            setStudent({ ...student, first_name: String(value) })
          }
        />

        <Input
          label="Фамилия"
          value={student.last_name || ""}
          onChange={(value) =>
            setStudent({ ...student, last_name: String(value) })
          }
        />

        <Input
          label="Номер класса"
          type="number"
          min={1}
          max={11}
          value={String(student.number_of_class)}
          onChange={(value) =>
            setStudent({
              ...student,
              number_of_class: Number(value),
            })
          }
        />

        <Input
          label="Телефон"
          value={student.phone || ""}
          onChange={(value) => setStudent({ ...student, phone: String(value) })}
        />

        <Input
          label="Имя родителя"
          value={student.parent_name || ""}
          onChange={(value) =>
            setStudent({
              ...student,
              parent_name: String(value),
            })
          }
        />

        <Input
          label="Телефон родителя"
          value={student.parent_phone || ""}
          onChange={(value) =>
            setStudent({
              ...student,
              parent_phone: String(value),
            })
          }
        />

        <div className={styles.fullWidth}>
          <Input
            label="Заметки"
            value={student.notes || ""}
            onChange={(value) =>
              setStudent({ ...student, notes: String(value) })
            }
          />
        </div>

        <div className={styles.actions}>
          <Button
            label="Создать"
            onClick={() => {
              createStudent(student);
              // navigate("/students");
            }}
          />
        </div>
      </div>
    </div>
  );
}
