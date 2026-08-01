import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { studentsApi } from "../../shared/api/students";
import type { Student } from "../../entities/student";
import { useLoader } from "../../shared/store/loader";

import styles from "./Students.module.css";

const PAGE_SIZE = 10;

export default function Students() {
  const { getAll } = studentsApi;

  const { show, hide } = useLoader();

  const [students, setStudents] = useState<Student[]>([]);
  const [currentPage, setCurrentPage] = useState(1);

  useEffect(() => {
    const fetchStudents = async () => {
      try {
        show();
        const students = await getAll();
        setStudents(students.data);
      } finally {
        hide();
      }
    };
    fetchStudents();
  }, []);

  const totalPages = Math.ceil(students.length / PAGE_SIZE);

  const startIndex = (currentPage - 1) * PAGE_SIZE;

  const currentStudents = students.slice(startIndex, startIndex + PAGE_SIZE);

  return (
    <div className={styles.main}>
      <h1 className={styles.title}>Ученики</h1>

      <div className={styles.tableWrapper}>
        <table className={styles.table}>
          <thead>
            <tr>
              <th>ФИО</th>
              <th>Класс</th>
              <th>Телефон</th>
              <th>Родитель</th>
              <th>Телефон родителя</th>
              <th>Заметки</th>
              <th>Действия</th>
            </tr>
          </thead>

          <tbody>
            {currentStudents.map((student) => (
              <tr key={student.id}>
                <td>
                  {student.last_name} {student.first_name}
                </td>

                <td>{student.number_of_class}</td>

                <td>{student.phone || "—"}</td>

                <td>{student.parent_name || "—"}</td>

                <td>{student.parent_phone || "—"}</td>

                <td>{student.notes || "—"}</td>

                <td className={styles.actions}>
                  <button className={styles.view}>
                    <Link
                      to={`/students/${student.id}/edit`}
                      className={styles.edit}
                    >
                      ✏️
                    </Link>
                  </button>

                  <button className={styles.delete}>🗑️</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className={styles.pagination}>
        <button
          disabled={currentPage === 1}
          onClick={() => setCurrentPage((prev) => prev - 1)}
        >
          ←
        </button>

        {Array.from({ length: totalPages }).map((_, index) => {
          const page = index + 1;

          return (
            <button
              key={page}
              className={currentPage === page ? styles.activePage : ""}
              onClick={() => setCurrentPage(page)}
            >
              {page}
            </button>
          );
        })}

        <button
          disabled={currentPage === totalPages}
          onClick={() => setCurrentPage((prev) => prev + 1)}
        >
          →
        </button>
      </div>
    </div>
  );
}
