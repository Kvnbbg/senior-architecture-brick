export type TaskStatus = "todo" | "in_progress" | "done";

export interface TaskCreate {
  readonly title: string;
  readonly description?: string;
  readonly dueDate?: string; // ISO date
}

export interface Task {
  readonly id: string;
  readonly title: string;
  readonly description: string | null;
  readonly status: TaskStatus;
  readonly createdAt: string;
  readonly updatedAt: string;
  readonly dueDate: string | null;
}

export const TASK_STATUSES: readonly TaskStatus[] = [
  "todo",
  "in_progress",
  "done",
] as const;
