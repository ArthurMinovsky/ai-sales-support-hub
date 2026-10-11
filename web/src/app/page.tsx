import { redirect } from "next/navigation";
import { isVerifiedSession } from "@/lib/session";

export default async function HomePage() {
  redirect((await isVerifiedSession()) ? "/search" : "/login");
}
