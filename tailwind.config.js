/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./frontend/templates/**/*.html",
    "./backend/apps/**/*.py"
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          parchment: "#fdf7ee",
          ink: "#19120f",
          accent: "#2f5d85",
          accentWarm: "#ae6838",
          danger: "#b23a48",
          success: "#1f7a4c"
        }
      },
      boxShadow: {
        folio: "0 14px 34px rgba(45, 28, 20, 0.18)"
      }
    }
  },
  plugins: []
};
