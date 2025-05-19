
import React from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { useToast } from '@/components/ui/use-toast';
import { supabase } from '@/lib/supabaseClient';

const ContactForm = () => {
  const { toast } = useToast();

  const handleContactSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(e.target);
    const name = formData.get('name');
    const email = formData.get('email');
    const message = formData.get('message');

    try {
      const { data, error } = await supabase
        .from('contacts') 
        .insert([{ name, email, message }]);

      if (error) {
        throw error;
      }

      toast({
        title: "Message Sent!",
        description: "Thank you for reaching out. We'll be in touch soon.",
        variant: "default",
      });
      e.target.reset();
    } catch (error) {
      console.error('Error submitting contact form:', error);
      toast({
        title: "Error Sending Message",
        description: "There was a problem submitting your message. Please try again.",
        variant: "destructive",
      });
    }
  };

  return (
    <motion.section 
      id="contact" 
      className="py-16 sm:py-24 bg-slate-800 text-white"
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      viewport={{ once: true, amount: 0.3 }}
      transition={{ duration: 0.8 }}
    >
      <div className="container mx-auto px-4">
        <div className="max-w-3xl mx-auto text-center">
          <h2 className="text-3xl sm:text-4xl font-bold mb-4 text-sky-400">Contact Us</h2>
          <p className="text-lg text-slate-300 mb-8">
            Interested in learning more or partnering with us? We'd love to hear from you.
          </p>
        </div>
        <motion.form 
          className="max-w-xl mx-auto bg-slate-700 p-8 rounded-xl shadow-2xl"
          onSubmit={handleContactSubmit}
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, amount: 0.5 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <div className="grid grid-cols-1 gap-6">
            <div>
              <label htmlFor="name" className="block text-sm font-medium text-slate-300">Full Name</label>
              <input type="text" name="name" id="name" required className="mt-1 block w-full px-4 py-2.5 bg-slate-600 border border-slate-500 rounded-md shadow-sm focus:ring-sky-500 focus:border-sky-500 text-white placeholder-slate-400" placeholder="Your Name" />
            </div>
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-slate-300">Email Address</label>
              <input type="email" name="email" id="email" required className="mt-1 block w-full px-4 py-2.5 bg-slate-600 border border-slate-500 rounded-md shadow-sm focus:ring-sky-500 focus:border-sky-500 text-white placeholder-slate-400" placeholder="you@example.com" />
            </div>
            <div>
              <label htmlFor="message" className="block text-sm font-medium text-slate-300">Message</label>
              <textarea name="message" id="message" rows="4" required className="mt-1 block w-full px-4 py-2.5 bg-slate-600 border border-slate-500 rounded-md shadow-sm focus:ring-sky-500 focus:border-sky-500 text-white placeholder-slate-400" placeholder="Your message..."></textarea>
            </div>
            <div>
              <Button type="submit" className="w-full bg-sky-500 hover:bg-sky-600 text-white font-semibold">
                Send Message
              </Button>
            </div>
          </div>
        </motion.form>
      </div>
    </motion.section>
  );
};

export default ContactForm;
  