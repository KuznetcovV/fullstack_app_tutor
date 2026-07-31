import styles from "./button.module.css";

export default function Button({
  label,
  onClick,
}: {
  label: string;
  onClick: () => void;
}) {
  return (
    <button className={styles.button} onClick={onClick}>
      {label}
    </button>
  );
}
