# Data Model: Frontend Specifications for Next.js Todo App

## User Entity

**Description**: Represents an authenticated individual with unique identity, containing profile information and authentication credentials handled by Better Auth

**Fields**:
- `id` (string): Unique identifier for the user
- `email` (string): User's email address (used for authentication)
- `name` (string): User's display name (optional)
- `isLoggedIn` (boolean): Current authentication status

**Validation**:
- Email must be in valid email format
- Email is required
- ID must be unique

**Relationships**:
- One User owns many Tasks

## Task Entity

**Description**: Represents a user's to-do item with properties like title, description, completion status, and due date

**Fields**:
- `id` (string): Unique identifier for the task
- `title` (string): Brief title of the task (required)
- `description` (string): Detailed description of the task (optional)
- `completed` (boolean): Completion status of the task
- `dueDate` (Date | null): Date when the task is due (optional)
- `createdAt` (Date): Timestamp when the task was created
- `updatedAt` (Date): Timestamp when the task was last updated
- `userId` (string): Reference to the user who owns this task

**Validation**:
- Title is required and must be at least 1 character
- Due date, if provided, must be a valid date
- UserId must reference an existing user

**Relationships**:
- One Task belongs to one User

## Session Entity

**Description**: Represents an authenticated state allowing access to protected resources and user-specific data

**Fields**:
- `token` (string): JWT token for authentication
- `expiresAt` (Date): Expiration timestamp for the token
- `userId` (string): Reference to the authenticated user

**Validation**:
- Token must be a valid JWT
- ExpiresAt must be in the future
- UserId must reference an existing user

**Relationships**:
- One Session belongs to one User

## UI State Entities

### LoadingState
- `isLoading` (boolean): Indicates if data is being loaded
- `operation` (string): Describes the current operation being performed

### ErrorState
- `hasError` (boolean): Indicates if an error occurred
- `errorMessage` (string): Description of the error
- `errorType` (string): Type/classification of the error

### FilterState
- `showCompleted` (boolean): Whether to show completed tasks
- `searchQuery` (string): Text to filter tasks by