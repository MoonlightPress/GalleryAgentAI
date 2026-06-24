import { createContext, useContext, useState, useCallback } from 'react'
import { DEFAULT_LANG, t as translate } from './translations'

const LanguageContext = createContext(null)

export function LanguageProvider({ children }) {
  // Chinese-first product: always open in the default language (zh) on load.
  // The toggle switches it for the session; a reload returns to Chinese.
  const [lang, setLang] = useState(DEFAULT_LANG)

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
