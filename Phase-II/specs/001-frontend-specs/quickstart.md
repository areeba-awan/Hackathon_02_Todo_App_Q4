# Quickstart Guide: Frontend Specifications for Next.js Todo App

## Prerequisites

- Node.js 18+ installed on your system
- npm or yarn package manager
- Git for version control
- A code editor of your choice

## Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Install dependencies**
   ```bash
   npm install
   # or
   yarn install
   ```

3. **Configure environment variables**
   Create a `.env.local` file in the root directory with the following:
   ```
   NEXT_PUBLIC_BASE_URL=http://localhost:3000
   AUTH_SECRET=your-secret-key-here
   BACKEND_API_URL=http://localhost:8000  # Replace with your backend URL
   ```

4. **Run the development server**
   ```bash
   npm run dev
   # or
   yarn dev
   ```

5. **Open your browser**
   Visit [http://localhost:3000](http://localhost:3000) to see the application

## Development Workflow

1. **Start development server**
   Run `npm run dev` to start the development server with hot reloading

2. **Make changes to components**
   Edit files in the `app/` directory for pages and layouts
   Edit files in the `components/` directory for reusable UI components

3. **Test authentication flow**
   - Navigate to `/login` to test the login functionality
   - Navigate to `/register` to test the registration functionality
   - Access protected routes to verify authentication protection

4. **Verify responsive behavior**
   - Use browser developer tools to simulate different screen sizes
   - Test the application on actual mobile and tablet devices
   - Verify that all components adapt appropriately to different screen sizes

## Environment Configuration

1. **Better Auth Configuration**
   - The application expects the auth configuration in `lib/auth.ts` or similar
   - Ensure the backend API endpoint is correctly configured
   - Verify that JWT handling is properly set up

2. **API Endpoint Configuration**
   - Update the `BACKEND_API_URL` in your environment variables to point to your backend service
   - Ensure CORS settings allow requests from your frontend domain

3. **Required Environment Variables**
   - `NEXT_PUBLIC_BASE_URL`: The base URL of your application
   - `AUTH_SECRET`: Secret key for JWT signing/verification
   - `BACKEND_API_URL`: URL of your backend API service

## Common Commands

- `npm run dev`: Start development server
- `npm run build`: Build the application for production
- `npm run start`: Start production server
- `npm run lint`: Run linting checks
- `npm run test`: Run tests (if configured)

## Troubleshooting

1. **Authentication Issues**
   - Verify that the backend authentication service is running
   - Check that the AUTH_SECRET matches between frontend and backend
   - Ensure proper CORS configuration

2. **API Connection Issues**
   - Verify BACKEND_API_URL is correctly set
   - Check that the backend service is accessible
   - Confirm that required headers are being sent with requests

3. **Build Issues**
   - Ensure all dependencies are installed (`npm install`)
   - Check for TypeScript errors that might prevent building
   - Verify environment variables are properly configured