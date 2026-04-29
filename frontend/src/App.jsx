import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Activity, Droplet, Heart, User, Eye, ActivitySquare } from "lucide-react";
import { predictDrinker } from "./api";

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1,
    },
  },
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { type: "spring", stiffness: 100 } },
};

function App() {
  const [formData, setFormData] = useState({
    gender: "Male",
    age: 40,
    height_cm: 165,
    weight_kg: 75,
    waist_cm: 91,
    vision_left: 1.2,
    vision_right: 1.5,
    systolic_bp: 120,
    diastolic_bp: 70,
    total_cholesterol: 136,
    hdl_cholesterol: 41,
    ldl_cholesterol: 74,
    triglycerides: 104,
    hemoglobin: 15.8,
    creatinine: 0.9,
    liver_ast: 41.5,
    liver_alt: 32.0,
    gamma_gtp: 68.0,
    smoking_status: 1.0,
  });

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: name === "gender" ? value : parseFloat(value),
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    try {
      const data = await predictDrinker(formData);
      setResult(data);
    } catch (err) {
      console.error(err);
      alert("Failed to connect to API");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 relative overflow-hidden font-sans pb-20">
      {/* Background Magic Glows */}
      <div className="absolute top-[-20%] left-[-10%] w-[50%] h-[50%] bg-indigo-500/20 rounded-full blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[-20%] right-[-10%] w-[50%] h-[50%] bg-rose-500/20 rounded-full blur-[120px] pointer-events-none" />

      <div className="max-w-6xl mx-auto px-6 pt-16 relative z-10">
        <motion.div
          initial={{ opacity: 0, y: -20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-16"
        >
          <h1 className="text-5xl font-extrabold tracking-tight bg-gradient-to-r from-indigo-400 to-rose-400 text-transparent bg-clip-text mb-4">
            Aura Health Analyzer
          </h1>
          <p className="text-slate-400 text-lg">
            AI-driven lifestyle predictions via advanced biochemical markers.
          </p>
        </motion.div>

        <div className="grid lg:grid-cols-3 gap-8 items-start">
          {/* Main Form */}
          <motion.div
            variants={containerVariants}
            initial="hidden"
            animate="visible"
            className="lg:col-span-2 bg-slate-900/50 backdrop-blur-xl border border-slate-800 rounded-3xl p-8 shadow-2xl"
          >
            <form onSubmit={handleSubmit} className="space-y-8">
              {/* Section 1: Demographics */}
              <motion.div variants={itemVariants}>
                <h3 className="text-xl font-semibold text-indigo-300 flex items-center mb-4">
                  <User className="mr-2 h-5 w-5" /> Demographics & Vitals
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <InputGroup label="Gender" name="gender" value={formData.gender} onChange={handleChange} type="select" options={["Male", "Female"]} />
                  <InputGroup label="Age" name="age" value={formData.age} onChange={handleChange} />
                  <InputGroup label="Height (cm)" name="height_cm" value={formData.height_cm} onChange={handleChange} />
                  <InputGroup label="Weight (kg)" name="weight_kg" value={formData.weight_kg} onChange={handleChange} />
                  <InputGroup label="Waist (cm)" name="waist_cm" value={formData.waist_cm} onChange={handleChange} />
                </div>
              </motion.div>

              {/* Section 2: Blood Pressure & Vision */}
              <motion.div variants={itemVariants}>
                <h3 className="text-xl font-semibold text-rose-300 flex items-center mb-4">
                  <Heart className="mr-2 h-5 w-5" /> Cardiovascular & Sensory
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <InputGroup label="Systolic BP" name="systolic_bp" value={formData.systolic_bp} onChange={handleChange} />
                  <InputGroup label="Diastolic BP" name="diastolic_bp" value={formData.diastolic_bp} onChange={handleChange} />
                  <InputGroup label="Vision L" name="vision_left" value={formData.vision_left} onChange={handleChange} />
                  <InputGroup label="Vision R" name="vision_right" value={formData.vision_right} onChange={handleChange} />
                </div>
              </motion.div>

              {/* Section 3: Blood Chemistry */}
              <motion.div variants={itemVariants}>
                <h3 className="text-xl font-semibold text-emerald-300 flex items-center mb-4">
                  <Droplet className="mr-2 h-5 w-5" /> Blood Chemistry
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <InputGroup label="Tot. Chol." name="total_cholesterol" value={formData.total_cholesterol} onChange={handleChange} />
                  <InputGroup label="HDL Chol." name="hdl_cholesterol" value={formData.hdl_cholesterol} onChange={handleChange} />
                  <InputGroup label="LDL Chol." name="ldl_cholesterol" value={formData.ldl_cholesterol} onChange={handleChange} />
                  <InputGroup label="Triglycerides" name="triglycerides" value={formData.triglycerides} onChange={handleChange} />
                  <InputGroup label="Hemoglobin" name="hemoglobin" value={formData.hemoglobin} onChange={handleChange} />
                  <InputGroup label="Creatinine" name="creatinine" value={formData.creatinine} onChange={handleChange} />
                </div>
              </motion.div>

              {/* Section 4: Liver Enzymes & Habits */}
              <motion.div variants={itemVariants}>
                <h3 className="text-xl font-semibold text-amber-300 flex items-center mb-4">
                  <ActivitySquare className="mr-2 h-5 w-5" /> Liver & Habits
                </h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <InputGroup label="AST (SGOT)" name="liver_ast" value={formData.liver_ast} onChange={handleChange} />
                  <InputGroup label="ALT (SGPT)" name="liver_alt" value={formData.liver_alt} onChange={handleChange} />
                  <InputGroup label="Gamma GTP" name="gamma_gtp" value={formData.gamma_gtp} onChange={handleChange} />
                  <InputGroup label="Smoking Stat" name="smoking_status" value={formData.smoking_status} onChange={handleChange} />
                </div>
              </motion.div>

              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                variants={itemVariants}
                className="w-full py-4 mt-6 rounded-xl bg-gradient-to-r from-indigo-500 to-purple-600 font-bold text-lg text-white shadow-lg shadow-indigo-500/30 hover:shadow-indigo-500/50 transition-all"
              >
                {loading ? "Analyzing Biomarkers..." : "Run Analysis"}
              </motion.button>
            </form>
          </motion.div>

          {/* Results Panel */}
          <div className="lg:col-span-1 h-full">
            <AnimatePresence mode="wait">
              {result ? (
                <motion.div
                  key="result"
                  initial={{ opacity: 0, scale: 0.9, rotateX: 20 }}
                  animate={{ opacity: 1, scale: 1, rotateX: 0 }}
                  exit={{ opacity: 0, scale: 0.9 }}
                  className="relative h-full min-h-[400px] flex flex-col items-center justify-center bg-slate-900 border border-slate-800 rounded-3xl p-8 overflow-hidden"
                >
                  {/* Magic Glowing Border Effect */}
                  <div className={`absolute inset-0 opacity-20 blur-2xl ${result.prediction_code === 1 ? 'bg-rose-500' : 'bg-emerald-500'}`} />
                  
                  <div className="relative z-10 text-center space-y-6">
                    <p className="text-slate-400 font-medium uppercase tracking-widest text-sm">Analysis Complete</p>
                    <h2 className={`text-4xl font-black ${result.prediction_code === 1 ? 'text-rose-400' : 'text-emerald-400'}`}>
                      {result.prediction}
                    </h2>
                    
                    {result.confidence && (
                      <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                          <span className="text-slate-400">Confidence Match</span>
                          <span className="text-white font-bold">{(result.confidence * 100).toFixed(1)}%</span>
                        </div>
                        <div className="w-full bg-slate-800 rounded-full h-3 overflow-hidden">
                          <motion.div
                            initial={{ width: 0 }}
                            animate={{ width: `${result.confidence * 100}%` }}
                            transition={{ duration: 1.5, ease: "easeOut" }}
                            className={`h-full ${result.prediction_code === 1 ? 'bg-rose-500' : 'bg-emerald-500'}`}
                          />
                        </div>
                      </div>
                    )}
                    
                    <p className="text-sm text-slate-500 pt-4 leading-relaxed">
                      This prediction is derived from an ensemble Stacking Classifier analyzing 20+ biochemical indicators.
                    </p>
                  </div>
                </motion.div>
              ) : (
                <motion.div
                  key="placeholder"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  className="h-full min-h-[400px] flex flex-col items-center justify-center bg-slate-900/30 border border-slate-800/50 border-dashed rounded-3xl p-8 text-center"
                >
                  <Activity className="h-12 w-12 text-slate-600 mb-4" />
                  <h3 className="text-lg font-medium text-slate-400">Awaiting Data Input</h3>
                  <p className="text-sm text-slate-600 mt-2">Fill the biochemical markers and run analysis to view the AI prediction here.</p>
                </motion.div>
              )}
            </AnimatePresence>
          </div>
        </div>
      </div>
    </div>
  );
}

// Reusable Input Component
const InputGroup = ({ label, name, value, onChange, type = "number", options }) => (
  <div className="flex flex-col space-y-1">
    <label className="text-xs font-medium text-slate-400 ml-1">{label}</label>
    {type === "select" ? (
      <select
        name={name}
        value={value}
        onChange={onChange}
        className="bg-slate-950/50 border border-slate-700/50 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all"
      >
        {options.map((opt) => (
          <option key={opt} value={opt}>
            {opt}
          </option>
        ))}
      </select>
    ) : (
      <input
        type="number"
        step="any"
        name={name}
        value={value}
        onChange={onChange}
        className="bg-slate-950/50 border border-slate-700/50 rounded-lg px-3 py-2 text-sm text-slate-200 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition-all placeholder:text-slate-600"
      />
    )}
  </div>
);

export default App;
