using System;
using System.IO;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace StardewModManager
{
    public partial class Main : Form
    {
        public Main()
        {
            InitializeComponent();
        }

        private void browse_Click(object sender, EventArgs e)
        {
            FolderBrowserDialog browser = new FolderBrowserDialog();
            DialogResult result = browser.ShowDialog();
            if( result == DialogResult.OK)
            {
                String foldername = browser.SelectedPath + "\\";
                currentLocation.Text = foldername;
                String[] dirs = Directory.GetDirectories(foldername, "*", SearchOption.TopDirectoryOnly);
                enabledList.Items.Clear();
                disabledList.Items.Clear();
                foreach(String i in dirs)
                {
                    String rel = i.Replace(foldername, "");
                    if (rel.Substring(0,1) == ".")
                    {
                        disabledList.Items.Add(rel.Substring(1));
                    }
                    else
                    {
                        enabledList.Items.Add(rel);
                    }
                }
            }
        }

        private void steamLoc_Click(object sender, EventArgs e)
        {
            String foldername = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Stardew Valley\\Mods\\";
            currentLocation.Text = foldername;
            String[] dirs = Directory.GetDirectories(foldername, "*", SearchOption.TopDirectoryOnly);
            enabledList.Items.Clear();
            disabledList.Items.Clear();
            foreach (String i in dirs)
            {
                String rel = i.Replace(foldername, "");
                if (rel.Substring(0, 1) == ".")
                {
                    disabledList.Items.Add(rel.Substring(1));
                }
                else
                {
                    enabledList.Items.Add(rel);
                }
            }
        }

        private void disableButton_Click(object sender, EventArgs e)
        {
            ListBox.SelectedObjectCollection c = enabledList.SelectedItems;
            List<Object> itemsToMove = new List<Object>();
            foreach(Object item in c)
            {
                itemsToMove.Add(item);
            }
            foreach(Object item in itemsToMove)
            {
                enabledList.Items.Remove(item);
                disabledList.Items.Add(item);
                Directory.Move(currentLocation.Text + item.ToString(), currentLocation.Text + "." + item.ToString());
            }
        }

        private void enableButton_Click(object sender, EventArgs e)
        {
            ListBox.SelectedObjectCollection c = disabledList.SelectedItems;
            List<Object> itemsToMove = new List<Object>();
            foreach (Object item in c)
            {
                itemsToMove.Add(item);
            }
            foreach (Object item in itemsToMove)
            {
                disabledList.Items.Remove(item);
                enabledList.Items.Add(item);
                Directory.Move(currentLocation.Text + "." + item.ToString(), currentLocation.Text + item.ToString());
            }
        }
    }
}
