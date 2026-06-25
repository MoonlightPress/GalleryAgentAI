import { createContext, useContext, useState, useCallback, useEffect } from 'react'
import { DEFAULT_LANG, t as translate } from './translations'

const LanguageContext = createContext(null)

// Map our lang codes to valid BCP-47 values for the document's lang attribute.
const HTML_LANG = { zh: 'zh-Hans', ja: 'ja', en: 'en' }

export function LanguageProvider({ children }) {
  // Chinese-first product: always open in the default language (zh) on load.
  // The toggle switches it for the session; a reload returns to Chinese.
  const [lang, setLang] = useState(DEFAULT_LANG)

  // Keep <html lang> in sync with the active language (it's set zh-Hans in
  // index.html for first paint; the toggle updates it live).
  useEffect(() => {
    document.documentElement.lang = HTML_LANG[lang] || lang
  }, [lang])

  const t = useCallback((key, vars) => translate(key, lang, vars), [lang])

  return (
    <LanguageContext.Provider value={{ lang, setLang, t }}>
      {children}
    </LanguageContext.Provider>
  )
}

// eslint-disable-next-line react-refresh/only-export-components -- hook colocated with its provider by design
export function useLanguage() {
  return useContext(LanguageContext)
}
