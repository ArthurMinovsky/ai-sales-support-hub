import "./globals.css";
import type { Metadata } from "next";

// A fresh CSP nonce must be applied during each response's server rendering.
export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Sales Support Hub",
  description: "Catalog-grounded product recommendation workspace for sales teams",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
