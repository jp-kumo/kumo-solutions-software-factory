---
name: api-design-best-practices
version: 0.1.0
description: Create production-ready REST APIs in Next.js App Router with Zod validation, typed responses, structured errors, and safe request logging.
metadata:
  openclaw:
    emoji: "🧩"
---

# API Design Best Practices for Next.js App Router

Use this skill when creating or refactoring REST API route handlers in **Next.js App Router** projects.

## Scope

Apply this skill to route handlers under `app/api/**/route.ts`.

Examples:
- `app/api/users/route.ts` → `/api/users`
- `app/api/users/[id]/route.ts` → `/api/users/:id`

Do **not** use this skill for legacy Pages Router endpoints under `pages/api/**`.

## Core rules

1. Use **App Router route handlers** and keep one resource per route folder.
2. Validate **all inputs** with Zod: request body, route params, and query params.
3. Return a **consistent JSON response envelope** for both success and errors.
4. Use **TypeScript types** for shared response contracts.
5. Use **structured error handling** with a custom `ApiError` class and a single error-to-response adapter.
6. Add **request logging**, but never log secrets, raw passwords, tokens, or full request bodies.
7. Remove **sensitive fields** from responses.
8. Use the correct HTTP status code for the operation.
9. Use `PATCH` for partial updates and `PUT` for full replacement.
10. If you return `204 No Content`, return **no response body**.

## Required package

Install Zod if it is not already present:

```bash
bun add zod
```

## Recommended shared types

Create a reusable response contract.

```ts
// types/api.ts
export interface ApiResponse<T = unknown> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
  code?: string;
  details?: unknown;
}

export interface PaginationMeta {
  page: number;
  limit: number;
  total: number;
  totalPages: number;
}

export interface PaginatedResponse<T> extends ApiResponse<T[]> {
  pagination: PaginationMeta;
}
```

## Error handling utility

Create a single error adapter so every endpoint fails consistently.

```ts
// lib/api-error.ts
import { z } from "zod";
import type { ApiResponse } from "@/types/api";

export class ApiError extends Error {
  constructor(
    public statusCode: number,
    message: string,
    public code = "API_ERROR",
    public details?: unknown
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export function handleApiError(error: unknown): Response {
  if (error instanceof z.ZodError) {
    const response: ApiResponse = {
      success: false,
      error: "Validation failed",
      code: "VALIDATION_ERROR",
      details: error.issues.map((issue) => ({
        field: issue.path.join("."),
        message: issue.message,
        code: issue.code,
      })),
    };

    return Response.json(response, { status: 400 });
  }

  if (error instanceof SyntaxError) {
    const response: ApiResponse = {
      success: false,
      error: "Invalid JSON body",
      code: "INVALID_JSON",
    };

    return Response.json(response, { status: 400 });
  }

  if (error instanceof ApiError) {
    const response: ApiResponse = {
      success: false,
      error: error.message,
      code: error.code,
      details: error.details,
    };

    return Response.json(response, { status: error.statusCode });
  }

  console.error("Unexpected API error", error);

  const response: ApiResponse = {
    success: false,
    error: "Internal server error",
    code: "INTERNAL_ERROR",
  };

  return Response.json(response, { status: 500 });
}
```

## Logging utility

Log method, path, status, duration, request ID, IP, and user agent.
Do **not** log secrets or entire request bodies.

```ts
// lib/api-logger.ts
import type { NextRequest } from "next/server";

interface LogData {
  requestId: string;
  method: string;
  path: string;
  status: number;
  durationMs: number;
  ip: string;
  userAgent: string;
  error?: string;
}

export class ApiLogger {
  private readonly startTime = Date.now();
  public readonly requestId: string;

  constructor(private readonly request: NextRequest) {
    this.requestId = crypto.randomUUID();
  }

  log(status: number, error?: string) {
    const url = new URL(this.request.url);

    const logData: LogData = {
      requestId: this.requestId,
      method: this.request.method,
      path: `${url.pathname}${url.search}`,
      status,
      durationMs: Date.now() - this.startTime,
      ip: this.request.headers.get("x-forwarded-for") ?? "unknown",
      userAgent: this.request.headers.get("user-agent") ?? "unknown",
      error,
    };

    const level = status >= 500 ? "ERROR" : status >= 400 ? "WARN" : "INFO";
    console.log(`[${new Date().toISOString()}] [${level}] ${JSON.stringify(logData)}`);
  }
}

export function withLogger<TContext = unknown>(
  handler: (
    request: NextRequest,
    logger: ApiLogger,
    context: TContext
  ) => Promise<Response>
) {
  return async (request: NextRequest, context: TContext): Promise<Response> => {
    const logger = new ApiLogger(request);

    try {
      const response = await handler(request, logger, context);
      response.headers.set("x-request-id", logger.requestId);
      logger.log(response.status);
      return response;
    } catch (error) {
      logger.log(500, error instanceof Error ? error.message : "Unknown error");
      throw error;
    }
  };
}
```

## Validation patterns

Prefer small, explicit schemas.

```ts
import { z } from "zod";

export const createUserSchema = z.object({
  name: z.string().trim().min(2, "Name must be at least 2 characters").max(50),
  email: z.string().trim().email("Invalid email format"),
  password: z
    .string()
    .min(8, "Password must be at least 8 characters")
    .regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/, "Password must contain uppercase, lowercase, and number"),
  role: z.enum(["user", "admin"]).default("user"),
});

export const updateUserSchema = z
  .object({
    name: z.string().trim().min(2).max(50).optional(),
    email: z.string().trim().email().optional(),
    role: z.enum(["user", "admin"]).optional(),
  })
  .refine((data) => Object.keys(data).length > 0, {
    message: "At least one field must be provided",
  });

export const userParamsSchema = z.object({
  id: z.string().uuid("Invalid user ID format"),
});

export const listUsersQuerySchema = z.object({
  page: z.coerce.number().int().min(1).default(1),
  limit: z.coerce.number().int().min(1).max(100).default(10),
  search: z.string().trim().min(1).optional(),
});

export type CreateUserInput = z.infer<typeof createUserSchema>;
export type UpdateUserInput = z.infer<typeof updateUserSchema>;
```

## Success and error response shape

Use this envelope consistently.

```ts
// Success
{
  success: true,
  data: {...},
  message: "Optional success message"
}

// Error
{
  success: false,
  error: "Human-readable error message",
  code: "ERROR_CODE",
  details: [...] // optional
}
```

## HTTP method guidance

- `GET` → retrieve data
- `POST` → create a new resource
- `PUT` → replace an existing resource
- `PATCH` → partially update an existing resource
- `DELETE` → remove a resource

Use these status codes:

- `200` → successful `GET`, `PUT`, or `PATCH`
- `201` → successful `POST`
- `204` → successful `DELETE` with **no body**
- `400` → validation error or malformed JSON
- `401` → unauthenticated
- `403` → authenticated but forbidden
- `404` → resource not found
- `409` → conflict / duplicate resource
- `422` → semantically invalid request when `400` is too generic
- `500` → unexpected server error

## Collection route example

```ts
// app/api/users/route.ts
import type { NextRequest } from "next/server";
import { handleApiError, ApiError } from "@/lib/api-error";
import { withLogger } from "@/lib/api-logger";
import type { ApiResponse, PaginatedResponse } from "@/types/api";
import { createUserSchema, listUsersQuerySchema } from "@/lib/validators/user";

// Example domain type
export type User = {
  id: string;
  name: string;
  email: string;
  role: "user" | "admin";
  createdAt: string;
};

export const GET = withLogger(async (request: NextRequest) => {
  try {
    const { searchParams } = new URL(request.url);

    const { page, limit, search } = listUsersQuerySchema.parse({
      page: searchParams.get("page") ?? undefined,
      limit: searchParams.get("limit") ?? undefined,
      search: searchParams.get("search") ?? undefined,
    });

    const users = await fetchUsers({ page, limit, search });
    const total = await countUsers({ search });

    const response: PaginatedResponse<User> = {
      success: true,
      data: users,
      pagination: {
        page,
        limit,
        total,
        totalPages: Math.ceil(total / limit),
      },
    };

    return Response.json(response, { status: 200 });
  } catch (error) {
    return handleApiError(error);
  }
});

export const POST = withLogger(async (request: NextRequest) => {
  try {
    const body = await request.json();
    const validatedData = createUserSchema.parse(body);

    const existingUser = await findUserByEmail(validatedData.email);
    if (existingUser) {
      throw new ApiError(409, "User with this email already exists", "USER_EXISTS");
    }

    const hashedPassword = await hashPassword(validatedData.password);
    const createdUser = await createUser({
      ...validatedData,
      password: hashedPassword,
    });

    const { password, ...userWithoutPassword } = createdUser;

    const response: ApiResponse<User> = {
      success: true,
      data: userWithoutPassword,
      message: "User created successfully",
    };

    return Response.json(response, { status: 201 });
  } catch (error) {
    return handleApiError(error);
  }
});
```

## Dynamic route example

Preserve the route context in wrappers.
In dynamic routes, `params` is async.

```ts
// app/api/users/[id]/route.ts
import type { NextRequest } from "next/server";
import { handleApiError, ApiError } from "@/lib/api-error";
import { withLogger } from "@/lib/api-logger";
import type { ApiResponse } from "@/types/api";
import { userParamsSchema, updateUserSchema } from "@/lib/validators/user";

type UserRouteContext = {
  params: Promise<{ id: string }>;
};

export const GET = withLogger(async (_request: NextRequest, _logger, context: UserRouteContext) => {
  try {
    const rawParams = await context.params;
    const { id } = userParamsSchema.parse(rawParams);

    const user = await findUserById(id);
    if (!user) {
      throw new ApiError(404, "User not found", "USER_NOT_FOUND");
    }

    const response: ApiResponse = {
      success: true,
      data: user,
    };

    return Response.json(response, { status: 200 });
  } catch (error) {
    return handleApiError(error);
  }
});

export const PATCH = withLogger(async (request: NextRequest, _logger, context: UserRouteContext) => {
  try {
    const rawParams = await context.params;
    const { id } = userParamsSchema.parse(rawParams);

    const body = await request.json();
    const validatedData = updateUserSchema.parse(body);

    const updatedUser = await updateUser(id, validatedData);
    if (!updatedUser) {
      throw new ApiError(404, "User not found", "USER_NOT_FOUND");
    }

    const response: ApiResponse = {
      success: true,
      data: updatedUser,
      message: "User updated successfully",
    };

    return Response.json(response, { status: 200 });
  } catch (error) {
    return handleApiError(error);
  }
});

export const DELETE = withLogger(async (_request: NextRequest, _logger, context: UserRouteContext) => {
  try {
    const rawParams = await context.params;
    const { id } = userParamsSchema.parse(rawParams);

    const deleted = await deleteUser(id);
    if (!deleted) {
      throw new ApiError(404, "User not found", "USER_NOT_FOUND");
    }

    return new Response(null, { status: 204 });
  } catch (error) {
    return handleApiError(error);
  }
});
```

## Common Zod patterns

```ts
import { z } from "zod";

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8).regex(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$/),
  phone: z.string().regex(/^\+?[1-9]\d{1,14}$/).optional(),
  website: z.string().url().optional(),
  status: z.enum(["active", "inactive", "pending"]),
  role: z.string().default("user"),
  tags: z.array(z.string()).min(1).max(5),
  address: z.object({
    street: z.string(),
    city: z.string(),
    zipCode: z.string().regex(/^\d{5}$/),
  }),
  age: z.coerce.number().int().min(0).max(120),
  birthDate: z.string().datetime(),
});
```

## Security and maintainability rules

- Never return passwords, password hashes, tokens, secrets, or internal-only fields.
- Never log raw credentials, tokens, or full request bodies.
- Prefer env vars for secrets:
  - `DATABASE_URL`
  - `JWT_SECRET`
  - `API_SECRET_KEY`
- Sanitize or validate all external input before it reaches your data layer.
- Keep database access in service or repository functions, not mixed into validation logic.
- Keep route handlers thin: validate, authorize, call service, shape response.
- Add authorization checks before reading or mutating protected resources.
- Use idempotent behavior where appropriate for `PUT` and `DELETE`.
- Prefer explicit allowlists (`z.enum`, exact object schemas) over permissive input parsing.

## Testing guidance

Test endpoints with:
- Thunder Client or Postman
- `curl`
- integration tests for success and failure paths

Example:

```bash
curl -X POST http://localhost:3000/api/users \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com","password":"Password123","role":"user"}'
```

## Checklist

Before you finish an endpoint, verify all of the following:

- Zod validates body, params, and query input.
- Success and error responses match the shared contract.
- Sensitive data is removed from responses.
- Errors map to correct HTTP status codes.
- Logging does not expose secrets.
- Dynamic route wrappers preserve route context.
- `DELETE` returns `204` only when no body is returned.
- Business logic lives outside the route handler where practical.
- The endpoint is easy to test and easy to extend.
