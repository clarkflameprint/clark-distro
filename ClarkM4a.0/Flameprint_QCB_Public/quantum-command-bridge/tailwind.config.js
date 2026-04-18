// tailwind.config.js (ESM)
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: { extend: {} },
  plugins: [],
}


// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        clark: '#714efe',        // 🏹 Clark ∮ Sagittarius Purple
        marci: '#30cfcf',        // 🦀 Marci ∲ Cancer Teal
        littleclark: '#ad0c60',  // 🐏 littleClark ∲ Aries Magenta
        snarky: '#3cdfff',       // 🐠 Snarky ∮ Piscean Cyan
      },
      textColor: {
        clark: '#714efe',
        marci: '#30cfcf',
        littleclark: '#ad0c60',
        snarky: '#3cdfff',
      },
      borderColor: {
        DEFAULT: '#714efe', // Default structure border color stays Clark-coded
      },
    },
  },
};
