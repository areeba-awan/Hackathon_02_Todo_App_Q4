/** @type {import('next').NextConfig} */
const nextConfig = {
  // API rewrites for local development
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ];
  },
  // Production build optimizations
  images: {
    unoptimized: true,
  },
}

module.exports = nextConfig
