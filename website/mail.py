from flask import Flask, Blueprint, redirect, url_for
from flask_mail import Message
from . import db, mail
from .models import Active, Walk
import os 

mailer = Blueprint('mailer', __name__) #Create the blueprint

def send_email(subject, recipients, body):
    msg = Message(
        subject=subject,
        recipients=recipients,
        body=body
    )
    mail.send(msg)

def send_email_html(subject, recipients, html):
    msg = Message(
        subject=subject,
        recipients=recipients,
        html=html
    )
    mail.send(msg)

def inform_pending(recipient, active_id):
    url = url_for("views.view_walk", active_id=active_id, _external=True)
    recipients = [recipient]
    subject = "Walk Requested!"
    message = f"""
                <!doctype html>
                <html lang="en">
                <body style="margin:0; padding:0; background:#f6f7fb; font-family: Arial, sans-serif;">
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f6f7fb; padding:24px 0;">
                    <tr>
                        <td align="center">
                        <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,0.08);">
                            <tr>
                            <td style="padding:28px 28px 12px 28px;">
                                <h2 style="margin:0 0 10px 0; font-size:20px; line-height:1.3; color:#111827;">
                                Walk has been requested
                                </h2>

                                <p style="margin:0 0 18px 0; font-size:14px; line-height:1.6; color:#374151;">
                                Click the button below to access walk.
                                </p>

                                <!-- Button -->
                                <table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 0 18px 0;">
                                <tr>
                                    <td bgcolor="#2563eb" style="border-radius:10px;">
                                    <a href="{url}"
                                        style="display:inline-block; padding:12px 18px; font-size:14px; color:#ffffff; text-decoration:none; font-weight:600;">
                                        Open page
                                    </a>
                                    </td>
                                </tr>
                                </table>

                                <p style="margin:0 0 10px 0; font-size:12px; line-height:1.6; color:#6b7280;">
                                If the button does not work, copy and paste this link into your browser:
                                </p>

                                <p style="margin:0 0 22px 0; font-size:12px; line-height:1.6;">
                                <a href="{url}" style="color:#2563eb; text-decoration:underline; word-break:break-all;">
                                    {url}
                                </a>
                                </p>

                                <hr style="border:none; border-top:1px solid #e5e7eb; margin:0 0 14px 0;">

                                <p style="margin:0; font-size:12px; line-height:1.6; color:#9ca3af;">
                                If you did not request this email, you can ignore it.
                                </p>
                            </td>
                            </tr>
                        </table>

                        <p style="margin:14px 0 0 0; font-size:11px; color:#9ca3af;">
                            © OpBlock. All rights reserved.
                        </p>
                        </td>
                    </tr>
                    </table>
                </body>
                </html>
                """
    send_email_html(subject, recipients, message)

def inform_invitation(walker, active_id):
    url1 = url_for("decisions.walker_accept", active_id=active_id, walker_id=walker.id, _external=True) 
    url2 = url_for("decisions.walker_reject", active_id=active_id, walker_id=walker.id, _external=True) 
    recipients = [walker.email]
    subject = "Walk Invitation!"
    message = f"""
                <!doctype html>
                <html lang="en">
                <body style="margin:0; padding:0; background:#f6f7fb; font-family: Arial, sans-serif;">
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f6f7fb; padding:24px 0;">
                    <tr>
                        <td align="center">
                        <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,0.08);">
                            <tr>
                            <td style="padding:28px 28px 12px 28px;">
                                <h2 style="margin:0 0 10px 0; font-size:20px; line-height:1.3; color:#111827;">
                                Walk has been requested
                                </h2>

                                <p style="margin:0 0 18px 0; font-size:14px; line-height:1.6; color:#374151;">
                                Click the button below to access walk.
                                </p>

                                <!-- Button -->
                                <table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 0 18px 0;">
                                <tr>
                                    <td bgcolor="#2563eb" style="border-radius:10px;">
                                    <a href="{url1}"
                                        style="display:inline-block; padding:12px 18px; font-size:14px; color:#ffffff; text-decoration:none; font-weight:600;">
                                        Accept
                                    </a>
                                    </td>
                                    <td bgcolor="#2563eb" style="border-radius:10px;">
                                    <a href="{url2}"
                                        style="display:inline-block; padding:12px 18px; font-size:14px; color:#ffffff; text-decoration:none; font-weight:600;">
                                        Reject
                                    </a>
                                    </td>
                                </tr>
                                </table>

                            </td>
                            </tr>
                        </table>

                        <p style="margin:14px 0 0 0; font-size:11px; color:#9ca3af;">
                            © OpBlock. All rights reserved.
                        </p>
                        </td>
                    </tr>
                    </table>
                </body>
                </html>
                """
    send_email_html(subject, recipients, message)

def inform_accepted(recipient, active_id):
    url = url_for("views.view_walk", active_id=active_id, _external=True)
    recipients = [recipient]
    subject = "Walk Accepted!"
    message = f"""
                <!doctype html>
                <html lang="en">
                <body style="margin:0; padding:0; background:#f6f7fb; font-family: Arial, sans-serif;">
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f6f7fb; padding:24px 0;">
                    <tr>
                        <td align="center">
                        <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,0.08);">
                            <tr>
                            <td style="padding:28px 28px 12px 28px;">
                                <h2 style="margin:0 0 10px 0; font-size:20px; line-height:1.3; color:#111827;">
                                Walk has been accepted
                                </h2>

                                <p style="margin:0 0 18px 0; font-size:14px; line-height:1.6; color:#374151;">
                                Track walk below
                                </p>

                                <!-- Button -->
                                <table role="presentation" cellpadding="0" cellspacing="0" style="margin:0 0 18px 0;">
                                <tr>
                                    <td bgcolor="#2563eb" style="border-radius:10px;">
                                    <a href="{url}"
                                        style="display:inline-block; padding:12px 18px; font-size:14px; color:#ffffff; text-decoration:none; font-weight:600;">
                                        Open walk
                                    </a>
                                    </td>
                                </tr>
                                </table>

                                <p style="margin:0 0 10px 0; font-size:12px; line-height:1.6; color:#6b7280;">
                                If the button does not work, copy and paste this link into your browser:
                                </p>

                                <p style="margin:0 0 22px 0; font-size:12px; line-height:1.6;">
                                <a href="{url}" style="color:#2563eb; text-decoration:underline; word-break:break-all;">
                                    {url}
                                </a>
                                </p>

                                <hr style="border:none; border-top:1px solid #e5e7eb; margin:0 0 14px 0;">

                                <p style="margin:0; font-size:12px; line-height:1.6; color:#9ca3af;">
                                If you did not request this email, you can ignore it.
                                </p>
                            </td>
                            </tr>
                        </table>

                        <p style="margin:14px 0 0 0; font-size:11px; color:#9ca3af;">
                            © OpBlock. All rights reserved.
                        </p>
                        </td>
                    </tr>
                    </table>
                </body>
                </html>
                """
    send_email_html(subject, recipients, message)

def inform_completed(recipient):
    recipients = [recipient]
    subject = "Walk Completed!"
    message = f"""
                <!doctype html>
                <html lang="en">
                <body style="margin:0; padding:0; background:#f6f7fb; font-family: Arial, sans-serif;">
                    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f6f7fb; padding:24px 0;">
                    <tr>
                        <td align="center">
                        <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="background:#ffffff; border-radius:12px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,0.08);">
                            <tr>
                            <td style="padding:28px 28px 12px 28px;">
                                <h2 style="margin:0 0 10px 0; font-size:20px; line-height:1.3; color:#111827;">
                                Walk has been completed
                                </h2>

                                <p style="margin:0 0 18px 0; font-size:14px; line-height:1.6; color:#374151;">
                                Thank you for using OpBlock
                                </p>

                                <hr style="border:none; border-top:1px solid #e5e7eb; margin:0 0 14px 0;">

                                <p style="margin:0; font-size:12px; line-height:1.6; color:#9ca3af;">
                                If you did not request this email, you can ignore it.
                                </p>
                            </td>
                            </tr>
                        </table>

                        <p style="margin:14px 0 0 0; font-size:11px; color:#9ca3af;">
                            © OpBlock. All rights reserved.
                        </p>
                        </td>
                    </tr>
                    </table>
                </body>
                </html>
                """
    send_email_html(subject, recipients, message)


@mailer.route("/inform/pending/<recipient>/<active_id>", methods=['GET', 'POST']) 
def sendPending(recipient, active_id):
    inform_pending(recipient, active_id)
    return redirect(url_for("views.view_walk", active_id=active_id))

@mailer.route("/inform/accepted/<recipient>/<active_id>", methods=['GET', 'POST']) 
def sendAccepted(recipient, active_id):
    inform_accepted(recipient, active_id)
    return redirect(url_for("views.view_walk", active_id=active_id))

@mailer.route("/inform/completed/<recipient>", methods=['GET', 'POST']) 
def sendCompleted(recipient):
    inform_completed(recipient)
    return redirect(url_for("views.home"))