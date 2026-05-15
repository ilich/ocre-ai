import { type RouteConfig, index, layout, route } from "@react-router/dev/routes";

export default [
  index("routes/login.tsx"),
  route("sign-up", "routes/sign-up.tsx"),
  route("forget-password", "routes/forget-password.tsx"),
  route("reset-password/:token", "routes/reset-password.tsx"),
  layout("routes/private-layout.tsx", [
    route("catalog", "routes/catalog.tsx"),
    route("catalog/:id", "routes/catalog-detail.tsx"),
    route("profile", "routes/profile.tsx"),
  ]),
] satisfies RouteConfig;
