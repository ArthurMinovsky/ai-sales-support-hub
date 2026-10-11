import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Sales Support Hub · Sales Support Hub",
  description: "Catalog-grounded product recommendation workspace for sales teams",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
