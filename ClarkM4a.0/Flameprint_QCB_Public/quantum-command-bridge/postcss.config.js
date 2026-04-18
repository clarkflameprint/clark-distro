import tailwind from '@tailwindcss/postcss'
// postcss.config.js
import tailwindcss from '@tailwindcss/postcss'
import autoprefixer from 'autoprefixer'

export default {
    plugins: [tailwindcss, autoprefixer],
}