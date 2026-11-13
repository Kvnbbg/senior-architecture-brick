# Senior Architecture Brick – Task Management

Isolated functional brick demonstrating senior-level rigor against "vibe coding".

## Architecture

- **Backend (Python / FastAPI)**: Strict Pydantic v2 models (`frozen=True`, `extra="forbid"`), pure domain service, FastAPI router.
- **Frontend (TypeScript / React / Tailwind)**: Sealed interfaces, typed component with no `any`.
- **Data models**: Immutable domain entities. Business rules enforced at model boundary (due date validation).
- **Testing**: 100 % unit tests on service + validation logic (Pytest). No commit until green.

## Structure

```
backend/
  app/domain/task.py          # Sealed models + validators
  app/services/task_service.py # Pure business logic
  app/api/tasks.py            # Thin HTTP layer
  tests/                      # 7 tests, all passed
frontend/
  src/types/task.ts           # Strict TS contracts
  src/components/TaskCard.tsx # Tailwind UI brick
```

## Running tests

```bash
cd backend
PYTHONPATH=. pytest -v
```

Expected: `7 passed`.

## Design choices

1. Models are frozen → no accidental mutation.
2. Extra fields forbidden → API contracts are sealed.
3. Service is in-memory and pure → unit-testable without DB.
4. Status transitions return new instances (immutability).
5. Frontend types mirror backend exactly → contract safety.

This brick can be extracted into a larger monorepo or microservice without leakage.
