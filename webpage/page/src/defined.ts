interface Env {
  readonly apiHost: string;
}

interface Window {
  readonly env: Env;
}

declare module "*.jpg";
