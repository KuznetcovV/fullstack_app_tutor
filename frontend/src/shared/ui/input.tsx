import styles from "./input.module.css";

export default function Input({
  label,
  value,
  type,
  min,
  max,
  onChange,
}: {
  label: string;
  value: string | number;
  type?: string;
  min?: number;
  max?: number;
  onChange: (value: string | number) => void;
}) {
  return (
    <div className={styles.input}>
      <label>{label}</label>
      <input
        type={type || "text"}
        value={value}
        min={min}
        max={max}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
}
