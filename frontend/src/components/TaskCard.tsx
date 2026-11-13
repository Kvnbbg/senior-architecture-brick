import React from "react";
import type { Task, TaskStatus } from "../types/task";

interface TaskCardProps {
  readonly task: Task;
  readonly onStatusChange: (id: string, status: TaskStatus) => void;
}

const statusStyles: Record<TaskStatus, string> = {
  todo: "bg-slate-100 text-slate-700 border-slate-200",
  in_progress: "bg-blue-100 text-blue-800 border-blue-200",
  done: "bg-emerald-100 text-emerald-800 border-emerald-200",
};

export const TaskCard: React.FC<TaskCardProps> = ({ task, onStatusChange }) => {
  return (
    <article
      className="rounded-xl border bg-white p-5 shadow-sm transition hover:shadow-md"
      data-testid="task-card"
    >
      <header className="mb-3 flex items-start justify-between gap-3">
        <h3 className="text-lg font-semibold text-slate-900">{task.title}</h3>
        <span
          className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium ${statusStyles[task.status]}`}
        >
          {task.status.replace("_", " ")}
        </span>
      </header>

      {task.description && (
        <p className="mb-4 text-sm text-slate-600">{task.description}</p>
      )}

      {task.dueDate && (
        <p className="mb-4 text-xs text-slate-500">Due: {task.dueDate}</p>
      )}

      <footer className="flex gap-2">
        {task.status !== "done" && (
          <button
            type="button"
            className="rounded-md bg-slate-900 px-3 py-1.5 text-xs font-medium text-white hover:bg-slate-800"
            onClick={() =>
              onStatusChange(
                task.id,
                task.status === "todo" ? "in_progress" : "done",
              )
            }
          >
            {task.status === "todo" ? "Start" : "Complete"}
          </button>
        )}
      </footer>
    </article>
  );
};
