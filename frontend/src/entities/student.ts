export interface Student {
  id: string;
  first_name: string;
  last_name: string;
  number_of_class: number;
  phone?: string;
  parent_name?: string;
  parent_phone?: string;
  notes?: string;
  is_active?: boolean;
}
