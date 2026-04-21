import type { ReactNode } from "react";

type LayoutProps = {
  title: string;
  subtitle?: string;
  children: ReactNode;
};

export default function Layout({ title, subtitle, children }: LayoutProps) {
  return (
    <main className="min-h-screen bg-neutral-50">
      <div className="border-b border-neutral-200 bg-white/80 backdrop-blur">
        <div className="mx-auto max-w-6xl px-6 py-8">
          <p className="text-xs font-semibold uppercase tracking-[0.2em] text-neutral-500">
            GAMMA
          </p>
          <h1 className="mt-2 text-3xl font-bold tracking-tight text-neutral-950">
            {title}
          </h1>
          {subtitle ? (
            <p className="mt-2 max-w-2xl text-sm text-neutral-600">{subtitle}</p>
          ) : null}
        </div>
      </div>

      <div className="mx-auto max-w-6xl px-6 py-8">{children}</div>
    </main>
  );
}