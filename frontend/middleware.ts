import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

// Paths that require authentication
const protectedPaths = ['/dashboard', '/blogs', '/settings'];

// Paths that should redirect to dashboard if already authenticated
const authPaths = ['/login', '/register'];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Get auth token from cookie (if using cookie-based auth)
  // or check localStorage on client side
  // Note: This is a simple implementation. For production,
  // use proper JWT validation or session management

  // Check if the path is protected
  const isProtectedPath = protectedPaths.some(path => pathname.startsWith(path));
  const isAuthPath = authPaths.some(path => pathname.startsWith(path));

  // For now, we'll let the client-side handle authentication
  // since we're using localStorage. In a production app,
  // you'd want to use httpOnly cookies and validate here.

  return NextResponse.next();
}

export const config = {
  matcher: [
    '/((?!api|_next/static|_next/image|favicon.ico).*)',
  ],
};
