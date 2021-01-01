
namespace StardewModManager
{
    partial class Main
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.locationTitle = new System.Windows.Forms.Label();
            this.browse = new System.Windows.Forms.Button();
            this.enabledList = new System.Windows.Forms.ListBox();
            this.disableButton = new System.Windows.Forms.Button();
            this.enableButton = new System.Windows.Forms.Button();
            this.disabledList = new System.Windows.Forms.ListBox();
            this.currentLocation = new System.Windows.Forms.Label();
            this.enabledTitle = new System.Windows.Forms.Label();
            this.disabledTitle = new System.Windows.Forms.Label();
            this.steamLoc = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // locationTitle
            // 
            this.locationTitle.AutoSize = true;
            this.locationTitle.Location = new System.Drawing.Point(12, 9);
            this.locationTitle.Name = "locationTitle";
            this.locationTitle.Size = new System.Drawing.Size(177, 13);
            this.locationTitle.TabIndex = 0;
            this.locationTitle.Text = "Stardew Valley Mod Folder Location";
            // 
            // browse
            // 
            this.browse.Location = new System.Drawing.Point(195, 4);
            this.browse.Name = "browse";
            this.browse.Size = new System.Drawing.Size(75, 23);
            this.browse.TabIndex = 2;
            this.browse.Text = "Browse...";
            this.browse.UseVisualStyleBackColor = true;
            this.browse.Click += new System.EventHandler(this.browse_Click);
            // 
            // enabledList
            // 
            this.enabledList.FormattingEnabled = true;
            this.enabledList.Location = new System.Drawing.Point(12, 92);
            this.enabledList.Name = "enabledList";
            this.enabledList.SelectionMode = System.Windows.Forms.SelectionMode.MultiExtended;
            this.enabledList.Size = new System.Drawing.Size(147, 329);
            this.enabledList.TabIndex = 3;
            // 
            // disableButton
            // 
            this.disableButton.Location = new System.Drawing.Point(166, 202);
            this.disableButton.Name = "disableButton";
            this.disableButton.Size = new System.Drawing.Size(75, 23);
            this.disableButton.TabIndex = 4;
            this.disableButton.Text = ">>";
            this.disableButton.UseVisualStyleBackColor = true;
            this.disableButton.Click += new System.EventHandler(this.disableButton_Click);
            // 
            // enableButton
            // 
            this.enableButton.Location = new System.Drawing.Point(166, 245);
            this.enableButton.Name = "enableButton";
            this.enableButton.Size = new System.Drawing.Size(75, 23);
            this.enableButton.TabIndex = 5;
            this.enableButton.Text = "<<";
            this.enableButton.UseVisualStyleBackColor = true;
            this.enableButton.Click += new System.EventHandler(this.enableButton_Click);
            // 
            // disabledList
            // 
            this.disabledList.FormattingEnabled = true;
            this.disabledList.Location = new System.Drawing.Point(250, 93);
            this.disabledList.Name = "disabledList";
            this.disabledList.SelectionMode = System.Windows.Forms.SelectionMode.MultiExtended;
            this.disabledList.Size = new System.Drawing.Size(147, 329);
            this.disabledList.TabIndex = 6;
            // 
            // currentLocation
            // 
            this.currentLocation.AutoSize = true;
            this.currentLocation.Location = new System.Drawing.Point(12, 37);
            this.currentLocation.MaximumSize = new System.Drawing.Size(400, 0);
            this.currentLocation.Name = "currentLocation";
            this.currentLocation.Size = new System.Drawing.Size(0, 13);
            this.currentLocation.TabIndex = 7;
            // 
            // enabledTitle
            // 
            this.enabledTitle.AutoSize = true;
            this.enabledTitle.Location = new System.Drawing.Point(12, 73);
            this.enabledTitle.Name = "enabledTitle";
            this.enabledTitle.Size = new System.Drawing.Size(46, 13);
            this.enabledTitle.TabIndex = 8;
            this.enabledTitle.Text = "Enabled";
            // 
            // disabledTitle
            // 
            this.disabledTitle.AutoSize = true;
            this.disabledTitle.Location = new System.Drawing.Point(247, 72);
            this.disabledTitle.Name = "disabledTitle";
            this.disabledTitle.Size = new System.Drawing.Size(48, 13);
            this.disabledTitle.TabIndex = 9;
            this.disabledTitle.Text = "Disabled";
            // 
            // steamLoc
            // 
            this.steamLoc.Location = new System.Drawing.Point(276, 4);
            this.steamLoc.Name = "steamLoc";
            this.steamLoc.Size = new System.Drawing.Size(131, 23);
            this.steamLoc.TabIndex = 10;
            this.steamLoc.Text = "Steam Location";
            this.steamLoc.UseVisualStyleBackColor = true;
            this.steamLoc.Click += new System.EventHandler(this.steamLoc_Click);
            // 
            // Main
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(419, 434);
            this.Controls.Add(this.steamLoc);
            this.Controls.Add(this.disabledTitle);
            this.Controls.Add(this.enabledTitle);
            this.Controls.Add(this.currentLocation);
            this.Controls.Add(this.disabledList);
            this.Controls.Add(this.enableButton);
            this.Controls.Add(this.disableButton);
            this.Controls.Add(this.enabledList);
            this.Controls.Add(this.browse);
            this.Controls.Add(this.locationTitle);
            this.Name = "Main";
            this.Text = "Stardew Valley Mod Manager";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label locationTitle;
        private System.Windows.Forms.Button browse;
        private System.Windows.Forms.ListBox enabledList;
        private System.Windows.Forms.Button disableButton;
        private System.Windows.Forms.Button enableButton;
        private System.Windows.Forms.ListBox disabledList;
        private System.Windows.Forms.Label currentLocation;
        private System.Windows.Forms.Label enabledTitle;
        private System.Windows.Forms.Label disabledTitle;
        private System.Windows.Forms.Button steamLoc;
    }
}

