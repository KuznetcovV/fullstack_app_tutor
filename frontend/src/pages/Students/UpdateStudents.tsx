import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { studentsApi } from "../../shared/api/students";
import type { Student } from "../../entities/student";
import { useLoader } from "../../shared/store/loader";

import Input from "../../shared/ui/input";
import Button from "../../shared/ui/button";

import styles from "./UpdateStudents.module.css";

export default function UpdateStudents() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { show, hide } = useLoader();

  const { getById, update } = studentsApi;

  const [student, setStudent] = useState<Omit<Student, "id">>({
    first_name: "",
    last_name: "",
    number_of_class: 1,
    phone: "",
    parent_name: "",
    parent_phone: "",
    notes: "",
  });

  useEffect(() => {
    const fetchStudent = async () => {
      if (!id) return;
      try {
        show();
        const student = await getById(id);
        setStudent(student.data);
      } finally {
        hide();
      }
    };
    fetchStudent();
  }, [id]);

  const handleUpdate = async () => {
    if (!id) return;

    await update(id, student);

    navigate("/students");
  };

  return (
    <div className={styles.main}>
      <h1 className={styles.title}>Редактирование ученика</h1>

      <div className={styles.form}>
        <Input
          label="Имя"
          value={student.first_name}
          onChange={(value) =>
            setStudent({
              ...student,
              first_name: String(value),
            })
          }
        />

        <Input
          label="Фамилия"
          value={student.last_name}
          onChange={(value) =>
            setStudent({
              ...student,
              last_name: String(value),
            })
          }
        />

        <Input
          label="Класс"
          type="number"
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
          onChange={(value) =>
            setStudent({
              ...student,
              phone: String(value),
            })
          }
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

        <div className={styles.full}>
          <Input
            label="Заметки"
            value={student.notes || ""}
            onChange={(value) =>
              setStudent({
                ...student,
                notes: String(value),
              })
            }
          />
        </div>

        <div className={styles.actions}>
          <Button label="Сохранить" onClick={handleUpdate} />
        </div>
      </div>
    </div>
  );
}
