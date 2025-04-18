/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}","./assets/*/*.js",
  ],
  theme: {
    extend: {
      colors:{
        "bluevio":"#6655FF",
        "mygray":"#7575cc",
        "bluebg":"rgba(15, 9, 37, 0.3)",
        "ft":"rgba(0,0,30,1)"
      }
    },
  },
  plugins: [],
}