import { type RouteConfig, index, route } from "@react-router/dev/routes";

export default [
  index("routes/login.tsx"),
  route("catalog", "routes/catalog.tsx"),
  route("sign-up", "routes/sign-up.tsx"),
  route("forget-password", "routes/forget-password.tsx"),
  route("reset-password/:token", "routes/reset-password.tsx"),
  route("profile", "routes/profile.tsx"),
] satisfies RouteConfig;
