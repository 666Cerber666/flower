/** @type {import('tailwindcss').Config} */
export default {
  content: [
    './index.html',
    './src/**/*.vue',
  ],
  theme: {
    extend: {
      width: {
        '450': '450px',
        '24': '24px',
        '32': '32px',
      },
    },
  },
  plugins: [],
}
