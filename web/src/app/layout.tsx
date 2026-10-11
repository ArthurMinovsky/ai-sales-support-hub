import "./globals.css";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AI Sales Support Hub",
  description: "Demo catalog recommendation workspace",
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return <html lang="en"><body>{children}</body></html>;
}
