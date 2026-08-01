import styles from "./input.module.css";

interface InputProps {
  label: string;
  value: string | number;
  type?: "text" | "email" | "password" | "number";
  min?: number;
  max?: number;
  onChange: (value: string | number) => void;
}

export default function Input({
  label,
  value,
  type = "text",
  min,
  max,
  onChange,
}: InputProps) {
  return (
    <fieldset className={styles.input}>
      <legend>{label}</legend>

      <input
        type={type}
        value={value}
        min={min}
        max={max}
        onChange={(e) => {
          const value = e.target.value;

          onChange(type === "number" ? Number(value) : value);
        }}
      />
    </fieldset>
  );
}
