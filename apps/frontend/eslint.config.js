import js from "@eslint/js";
import globals from "globals";
import tseslint from "typescript-eslint";
import reactHooks from "eslint-plugin-react-hooks";
import reactRefresh from "eslint-plugin-react-refresh";
import prettier from "eslint-config-prettier";

export default tseslint.config(
  { ignores: ["build", ".react-router"] },

  // Base JS + TS rules
  js.configs.recommended,
  ...tseslint.configs.recommended,

  // React rules
  {
    plugins: {
      "react-hooks": reactHooks,
      "react-refresh": reactRefresh,
    },
    rules: {
      ...reactHooks.configs.recommended.rules,

      // react-hooks@7 new rule — flags setLoading(true) at the top of async
      // effects, which is a common and intentional pattern for loading state.
      "react-hooks/set-state-in-effect": "off",

      // React Router v7 route files always export meta/clientLoader alongside
      // the default component — this is the framework convention.
      "react-refresh/only-export-components": [
        "warn",
        {
          allowConstantExport: true,
          allowExportNames: [
            "meta",
            "links",
            "headers",
            "loader",
            "action",
            "clientLoader",
            "clientAction",
            "handle",
            "shouldRevalidate",
          ],
        },
      ],
    },
  },

  // Project-wide settings
  {
    languageOptions: {
      globals: globals.browser,
    },
    rules: {
      "@typescript-eslint/no-unused-vars": [
        "warn",
        { argsIgnorePattern: "^_", varsIgnorePattern: "^_" },
      ],
      "@typescript-eslint/no-explicit-any": "warn",
      "@typescript-eslint/no-empty-object-type": "warn",

      // Allow ternary expressions used purely for side effects, e.g.:
      //   condition ? doA() : doB();
      "@typescript-eslint/no-unused-expressions": [
        "error",
        { allowTernary: true, allowShortCircuit: true },
      ],
    },
  },

  // Prettier — must be last to disable conflicting format rules
  prettier
);
