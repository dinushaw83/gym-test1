import type { Metadata } from "next";
import "./globals.css";
import { InstrumentationLoader } from "@/lib/utils/instrumentation-loader";

export const metadata: Metadata = {
  title: "proj3",
  description: "proj3 Application",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <InstrumentationLoader />
        {children}
      </body>
    </html>
  );
}

