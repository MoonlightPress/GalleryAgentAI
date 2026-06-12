// Per-page string registries so parallel page work never touches translations.js.
// Usage in a page:
//   import { strings } from './strings'
//   const t2 = useLocalT(strings)        // falls back to the global dictionary
import { useCallback } from 'react'
import { useLanguage } from './LanguageContext'

export function useLocalT(strings) {
  const { t, lang } = useLanguage()
  return useCallback((key, vars) => {
    const str = strings?.[lang]?.[key] ?? strings?.en?.[key]
    if (str === undefined) return t(key, vars)
    if (!vars) return str
    return Object.entries(vars).reduce((s, [k, v]) => s.replaceAll(`{${k}}`, v), str)
  }, [strings, lang, t])
}
