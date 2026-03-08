import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/contexts/AuthContext";
import { useToast } from "@/hooks/use-toast";

export default function AuthPage() {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [username, setUsername] = useState("");
  const [fullName, setFullName] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const navigate = useNavigate();
  const { login, register } = useAuth();
  const { toast } = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      if (isLogin) {
        // Login
        await login(email, password);
        toast({
          title: "Success!",
          description: "You have been logged in successfully.",
        });
        navigate("/");
      } else {
        // Register
        if (password !== confirmPassword) {
          toast({
            title: "Error",
            description: "Passwords do not match",
            variant: "destructive",
          });
          setIsLoading(false);
          return;
        }

        if (password.length < 8) {
          toast({
            title: "Error",
            description: "Password must be at least 8 characters",
            variant: "destructive",
          });
          setIsLoading(false);
          return;
        }

        await register({
          email,
          password,
          username,
          full_name: fullName || undefined,
        });

        toast({
          title: "Success!",
          description: "Your account has been created successfully.",
        });
        navigate("/");
      }
    } catch (error: any) {
      toast({
        title: "Error",
        description: error.message || "An error occurred. Please try again.",
        variant: "destructive",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setEmail("");
    setPassword("");
    setUsername("");
    setFullName("");
    setConfirmPassword("");
  };

  const toggleMode = () => {
    setIsLogin(!isLogin);
    resetForm();
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-orange-100 via-gray-100 to-purple-200">

      <div className="w-[420px] bg-white rounded-xl shadow-xl p-8">

        <div className="text-center mb-6">
          <h1 className="text-3xl font-bold text-gray-800">
            {isLogin ? "Login" : "Register"}
          </h1>
          <p className="text-gray-500 text-sm mt-2">
            {isLogin
              ? "Welcome back! Please login to your account."
              : "Create a new account to get started."}
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">

          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-400"
          />

          {!isLogin && (
            <>
              <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                minLength={3}
                maxLength={50}
                className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-400"
              />

              <input
                type="text"
                placeholder="Full Name (Optional)"
                value={fullName}
                onChange={(e) => setFullName(e.target.value)}
                className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-400"
              />
            </>
          )}

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={8}
            className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-400"
          />

          {!isLogin && (
            <input
              type="password"
              placeholder="Confirm Password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              className="w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-400"
            />
          )}

          {isLogin && (
            <div className="text-right text-sm text-orange-500 cursor-pointer hover:underline">
              Forgot your password?
            </div>
          )}

          <button
            type="submit"
            disabled={isLoading}
            className="w-full bg-indigo-500 hover:bg-indigo-600 disabled:bg-gray-400 text-white py-3 rounded-lg font-medium transition-colors"
          >
            {isLoading
              ? "Please wait..."
              : isLogin
              ? "Login"
              : "Register"}
          </button>

        </form>

        <div className="text-center text-gray-500 my-4">
          Or Login With
        </div>

        <div className="flex gap-3">

          <button className="flex-1 border rounded-lg py-2 flex items-center justify-center gap-2 hover:bg-gray-100">
            <img src="https://www.svgrepo.com/show/475656/google-color.svg" className="w-5"/>
            Google
          </button>

          <button className="flex-1 border rounded-lg py-2 flex items-center justify-center gap-2 hover:bg-gray-100">
            <img src="https://www.svgrepo.com/show/448224/facebook.svg" className="w-5"/>
            Facebook
          </button>

        </div>

        <div className="text-center text-sm text-gray-500 mt-6">
          {isLogin ? (
            <>
              Don't have an account?{" "}
              <span
                className="text-indigo-500 cursor-pointer hover:underline"
                onClick={toggleMode}
              >
                Sign up
              </span>
            </>
          ) : (
            <>
              Already have an account?{" "}
              <span
                className="text-indigo-500 cursor-pointer hover:underline"
                onClick={toggleMode}
              >
                Login
              </span>
            </>
          )}
        </div>

      </div>
    </div>
  );
}