
import React from 'react';
import { Linkedin, Twitter, Github, Mail } from 'lucide-react';

const Footer = () => {
  return (
    <footer className="bg-slate-900 text-slate-400 py-12">
      <div className="container mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-6 md:mb-0 text-center md:text-left">
            <p className="text-sm">&copy; {new Date().getFullYear()} LangGraphSemantic. All rights reserved.</p>
            <p className="text-xs mt-1">Pioneering AI Content Solutions.</p>
          </div>
          <div className="flex space-x-5">
            <a href="#" aria-label="LinkedIn" className="text-slate-400 hover:text-sky-400 transition-colors duration-300">
              <Linkedin size={20} />
            </a>
            <a href="#" aria-label="Twitter" className="text-slate-400 hover:text-sky-400 transition-colors duration-300">
              <Twitter size={20} />
            </a>
            <a href="#" aria-label="GitHub" className="text-slate-400 hover:text-sky-400 transition-colors duration-300">
              <Github size={20} />
            </a>
            <a href="mailto:contact@langgraphsemantic.com" aria-label="Email" className="text-slate-400 hover:text-sky-400 transition-colors duration-300">
              <Mail size={20} />
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
  