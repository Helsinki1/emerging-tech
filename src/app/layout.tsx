import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link"
import Image from "next/image"
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Create Next App",
  description: "Generated by create next app",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <nav className="bg-gradient-to-r from-orange-500 via-rose-400 to-orange-400 w-full h-20 flex justify-between items-center p-4 bg-orange-500">
          <Link href="/" className="justify-start ml-32">
            <h1 className="text-4xl text-white font-bold font-sans">Semantic Scout</h1>
          </Link>
          <div className="flex space-x-16 pr-14">
            <Link href="/opensrc" className="text-2xl font-bold">Open Source</Link>
            <Link href="/jobs" className="text-2xl font-bold">Research</Link>
            <Link href="/deals" className="text-2xl font-bold">Our Sources</Link>
          </div>
        </nav>
        {children}
      </body>
    </html>
  );
}
